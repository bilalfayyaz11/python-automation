RESOURCE_LIMITS = {
    "cpu_percent": 80.0,
    "memory_percent": 85.0,
    "disk_percent": 90.0,
}

POLICY_RULES = {
    "max_request_size": 1048576,
    "allowed_methods": ["GET", "POST", "PUT", "DELETE"],
    "rate_limit_per_minute": 100,
}

API_CONFIG = {
    "title": "Status and Policy Service",
    "version": "1.0.0",
    "description": "System monitoring and policy enforcement API",
}
