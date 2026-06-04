from datetime import datetime, timezone
from typing import Dict

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from config import API_CONFIG, POLICY_RULES, RESOURCE_LIMITS
from models import HealthResponse, PolicyCheckRequest, PolicyCheckResponse, SystemStatus
from policies import (
    check_system_health,
    enforce_rate_limit,
    validate_http_method,
    validate_request_size,
)

app = FastAPI(
    title=API_CONFIG["title"],
    version=API_CONFIG["version"],
    description=API_CONFIG["description"],
)

request_tracker: Dict[str, int] = {}


def utc_now() -> datetime:
    """Return timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - basic health check."""
    return HealthResponse(
        status="ok",
        timestamp=utc_now(),
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint."""
    return HealthResponse(
        status="ok",
        timestamp=utc_now(),
    )


@app.get("/status", response_model=SystemStatus)
async def get_system_status():
    """
    Get current system resource usage and status.
    """
    system_status, metrics = check_system_health()

    return SystemStatus(
        timestamp=utc_now(),
        cpu_percent=metrics["cpu_percent"],
        memory_percent=metrics["memory_percent"],
        disk_percent=metrics["disk_percent"],
        status=system_status,
    )


@app.post("/policy/check", response_model=PolicyCheckResponse)
async def check_policy(policy_request: PolicyCheckRequest):
    """
    Check if a request complies with defined policies.
    """
    user_id = policy_request.user_id
    request_tracker[user_id] = request_tracker.get(user_id, 0) + policy_request.request_count

    size_allowed, size_reason = validate_request_size(policy_request.request_size)

    if not size_allowed:
        return PolicyCheckResponse(
            allowed=False,
            reason=size_reason,
            policy_name="max_request_size",
            timestamp=utc_now(),
        )

    method_allowed, method_reason = validate_http_method(policy_request.method)

    if not method_allowed:
        return PolicyCheckResponse(
            allowed=False,
            reason=method_reason,
            policy_name="allowed_methods",
            timestamp=utc_now(),
        )

    rate_allowed, rate_reason = enforce_rate_limit(
        user_id=user_id,
        request_count=request_tracker[user_id],
    )

    if not rate_allowed:
        return PolicyCheckResponse(
            allowed=False,
            reason=rate_reason,
            policy_name="rate_limit_per_minute",
            timestamp=utc_now(),
        )

    return PolicyCheckResponse(
        allowed=True,
        reason="Request satisfies all configured policies",
        policy_name="all_policies",
        timestamp=utc_now(),
    )


@app.get("/policies")
async def list_policies():
    """List all active policy rules."""
    return POLICY_RULES


@app.get("/limits")
async def get_resource_limits():
    """Get configured resource limit thresholds."""
    return RESOURCE_LIMITS


@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all incoming requests.
    """
    started_at = utc_now()
    print(f"[{started_at.isoformat()}] Incoming request: {request.method} {request.url.path}")

    response = await call_next(request)

    finished_at = utc_now()
    print(
        f"[{finished_at.isoformat()}] Completed request: "
        f"{request.method} {request.url.path} -> {response.status_code}"
    )

    return response


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Return structured response for unhandled exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "detail": str(exc),
            "path": request.url.path,
            "timestamp": utc_now().isoformat(),
        },
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
