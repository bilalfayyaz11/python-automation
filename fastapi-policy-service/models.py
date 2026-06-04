from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class SystemStatus(BaseModel):
    """Model for system status response."""

    timestamp: datetime
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    status: str


class PolicyCheckRequest(BaseModel):
    """Model for policy check requests."""

    request_size: int = Field(..., ge=0, description="Request size in bytes")
    method: str = Field(..., min_length=3, description="HTTP method")
    user_id: str = Field(..., min_length=1, description="User identifier")
    request_count: Optional[int] = Field(
        default=1,
        ge=0,
        description="Request count in current rate-limit window",
    )


class PolicyCheckResponse(BaseModel):
    """Model for policy check responses."""

    allowed: bool
    reason: str
    policy_name: str
    timestamp: datetime


class HealthResponse(BaseModel):
    """Model for health check response."""

    status: str
    timestamp: datetime
    service: str = "FastAPI Policy Service"
