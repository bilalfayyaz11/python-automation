"""Typed configuration loader with schema validation and defaults."""

import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from pydantic import BaseModel, Field, ValidationError, field_validator


class DatabaseConfig(BaseModel):
    """Database connection configuration."""

    host: str = Field(default="localhost")
    port: int = Field(default=5432, ge=1, le=65535)
    username: str
    password: str
    database: str
    max_connections: int = Field(default=10, ge=1, le=100)

    @field_validator("host")
    @classmethod
    def validate_host(cls, value: str) -> str:
        """Validate database host."""
        if not value or not value.strip():
            raise ValueError("database.host cannot be empty")

        hostname_pattern = r"^[a-zA-Z0-9.-]+$"
        ip_pattern = r"^(\d{1,3}\.){3}\d{1,3}$"

        if value == "localhost":
            return value

        if re.match(ip_pattern, value):
            octets = value.split(".")
            if all(0 <= int(octet) <= 255 for octet in octets):
                return value
            raise ValueError("database.host contains an invalid IP address")

        if re.match(hostname_pattern, value):
            return value

        raise ValueError("database.host must be localhost, a hostname, or an IP address")


class CacheConfig(BaseModel):
    """Cache configuration."""

    enabled: bool = Field(default=True)
    ttl_seconds: int = Field(default=300, ge=0)
    max_size_mb: int = Field(default=100, ge=1)

    @field_validator("max_size_mb")
    @classmethod
    def validate_max_size(cls, value: int) -> int:
        """Validate cache size limit."""
        if value > 1024:
            raise ValueError("cache.max_size_mb cannot exceed 1024")
        return value


class LoggingConfig(BaseModel):
    """Logging configuration."""

    level: str = Field(default="INFO")
    format: str = Field(default="json")
    output_path: Optional[str] = Field(default="/var/log/app.log")

    @field_validator("level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        """Validate log level."""
        allowed_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        normalized_value = value.upper()

        if normalized_value not in allowed_levels:
            raise ValueError(
                "logging.level must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )

        return normalized_value

    @field_validator("format")
    @classmethod
    def validate_log_format(cls, value: str) -> str:
        """Validate log format."""
        allowed_formats = {"json", "text"}
        normalized_value = value.lower()

        if normalized_value not in allowed_formats:
            raise ValueError("logging.format must be either json or text")

        return normalized_value


class AppConfig(BaseModel):
    """Main application configuration."""

    app_name: str
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    database: DatabaseConfig
    cache: CacheConfig = Field(default_factory=CacheConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)

    @field_validator("app_name")
    @classmethod
    def validate_app_name(cls, value: str) -> str:
        """Validate application name."""
        if not value or not value.strip():
            raise ValueError("app_name cannot be empty")
        return value

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, value: str) -> str:
        """Validate deployment environment."""
        allowed_environments = {"development", "staging", "production"}

        if value not in allowed_environments:
            raise ValueError(
                "environment must be one of: development, staging, production"
            )

        return value


class ConfigLoader:
    """Configuration loader with type validation."""

    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config: Optional[AppConfig] = None

    def load(self) -> AppConfig:
        """Load and validate configuration from a JSON or YAML file."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        file_extension = Path(self.config_path).suffix.lower()

        if file_extension == ".json":
            config_dict = self._load_json(self.config_path)
        elif file_extension in {".yaml", ".yml"}:
            config_dict = self._load_yaml(self.config_path)
        else:
            raise ValueError("Unsupported configuration format. Use JSON, YAML, or YML.")

        self.config = self.validate_config(config_dict)
        return self.config

    def _load_json(self, file_path: str) -> Dict[str, Any]:
        """Load JSON configuration file."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("JSON configuration root must be an object")

            return data

        except json.JSONDecodeError as error:
            raise ValueError(f"Invalid JSON file: {error}") from error

    def _load_yaml(self, file_path: str) -> Dict[str, Any]:
        """Load YAML configuration file."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)

            if not isinstance(data, dict):
                raise ValueError("YAML configuration root must be a mapping/object")

            return data

        except yaml.YAMLError as error:
            raise ValueError(f"Invalid YAML file: {error}") from error

    def validate_config(self, config_dict: Dict[str, Any]) -> AppConfig:
        """Validate configuration dictionary using AppConfig schema."""
        try:
            return AppConfig(**config_dict)
        except ValidationError as error:
            messages = []

            for item in error.errors():
                location = ".".join(str(part) for part in item["loc"])
                message = item["msg"]
                messages.append(f"{location}: {message}")

            raise ValueError("Configuration validation failed: " + "; ".join(messages)) from error

    def get_config(self) -> AppConfig:
        """Return loaded configuration."""
        if self.config is None:
            raise RuntimeError("Configuration not loaded. Call load() first.")
        return self.config

    def reload(self) -> AppConfig:
        """Reload configuration from file."""
        return self.load()
