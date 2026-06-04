from typing import Dict, Tuple

import psutil

from config import POLICY_RULES, RESOURCE_LIMITS


def check_system_health() -> Tuple[str, Dict[str, float]]:
    """
    Check system resource usage and determine health status.
    """
    metrics = {
        "cpu_percent": psutil.cpu_percent(interval=0.2),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
    }

    critical = any(
        metrics[key] >= RESOURCE_LIMITS[key]
        for key in RESOURCE_LIMITS
    )

    warning = any(value >= 70.0 for value in metrics.values())

    if critical:
        status = "critical"
    elif warning:
        status = "warning"
    else:
        status = "healthy"

    return status, metrics


def validate_request_size(size_bytes: int) -> Tuple[bool, str]:
    """
    Validate if request size is within policy limits.
    """
    max_size = POLICY_RULES["max_request_size"]

    if size_bytes > max_size:
        return False, f"Request size {size_bytes} exceeds limit of {max_size} bytes"

    return True, "Request size is within allowed limit"


def validate_http_method(method: str) -> Tuple[bool, str]:
    """
    Validate if HTTP method is allowed by policy.
    """
    normalized_method = method.upper()
    allowed_methods = POLICY_RULES["allowed_methods"]

    if normalized_method not in allowed_methods:
        return False, f"HTTP method {normalized_method} is not allowed"

    return True, f"HTTP method {normalized_method} is allowed"


def enforce_rate_limit(user_id: str, request_count: int) -> Tuple[bool, str]:
    """
    Check if user has exceeded rate limit.
    """
    limit = POLICY_RULES["rate_limit_per_minute"]

    if request_count > limit:
        return False, f"User {user_id} exceeded rate limit of {limit} requests per minute"

    return True, f"User {user_id} is within rate limit"
