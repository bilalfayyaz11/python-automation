"""Test suite for typed configuration loader."""

import json
import os
import tempfile

from config_loader import AppConfig, ConfigLoader


def test_valid_yaml_config():
    """Test loading valid YAML configuration."""
    loader = ConfigLoader("configs/valid_config.yaml")
    config = loader.load()

    assert config.app_name == "MyApp"
    assert config.environment == "production"
    assert config.debug is False
    assert config.database.host == "db.example.com"
    assert config.database.port == 5432
    assert config.database.max_connections == 20
    assert config.cache.enabled is True
    assert config.cache.ttl_seconds == 600
    assert config.cache.max_size_mb == 256
    assert config.logging.level == "INFO"
    assert config.logging.format == "json"

    print("Valid YAML configuration loaded successfully")


def test_minimal_config_with_defaults():
    """Test configuration with default values."""
    loader = ConfigLoader("configs/minimal_config.json")
    config = loader.load()

    assert config.app_name == "MinimalApp"
    assert config.environment == "development"
    assert config.debug is False
    assert config.database.host == "localhost"
    assert config.database.port == 5432
    assert config.database.max_connections == 10
    assert config.cache.enabled is True
    assert config.cache.ttl_seconds == 300
    assert config.cache.max_size_mb == 100
    assert config.logging.level == "INFO"
    assert config.logging.format == "json"
    assert config.logging.output_path == "/var/log/app.log"

    print("Default values applied correctly")
    print("database.host:", config.database.host)
    print("database.port:", config.database.port)
    print("cache.enabled:", config.cache.enabled)
    print("cache.ttl_seconds:", config.cache.ttl_seconds)
    print("logging.level:", config.logging.level)


def test_invalid_config_detection():
    """Test invalid configuration detection."""
    loader = ConfigLoader("configs/invalid_config.yaml")

    try:
        loader.load()
        raise AssertionError("Invalid configuration should have failed validation")
    except ValueError as error:
        error_text = str(error)
        assert "environment" in error_text
        assert "database.host" in error_text
        assert "database.port" in error_text
        print("Invalid configuration detected correctly")
        print(error_text)


def test_missing_required_fields():
    """Test missing required fields."""
    missing_app_name = {
        "database": {
            "username": "user",
            "password": "pass",
            "database": "db",
        }
    }

    missing_database_username = {
        "app_name": "BrokenApp",
        "database": {
            "password": "pass",
            "database": "db",
        }
    }

    try:
        AppConfig(**missing_app_name)
        raise AssertionError("Missing app_name should have failed validation")
    except Exception as error:
        assert "app_name" in str(error)
        print("Missing app_name detected correctly")

    try:
        AppConfig(**missing_database_username)
        raise AssertionError("Missing database.username should have failed validation")
    except Exception as error:
        assert "username" in str(error)
        print("Missing database.username detected correctly")


def test_config_reload():
    """Test configuration reload functionality."""
    config_data = {
        "app_name": "ReloadApp",
        "environment": "development",
        "database": {
            "username": "reload_user",
            "password": "reload_pass",
            "database": "reload_db",
        },
    }

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as temp_file:
        json.dump(config_data, temp_file)
        temp_path = temp_file.name

    try:
        loader = ConfigLoader(temp_path)
        config = loader.load()
        assert config.app_name == "ReloadApp"

        config_data["app_name"] = "ReloadedApp"

        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(config_data, file)

        reloaded_config = loader.reload()
        assert reloaded_config.app_name == "ReloadedApp"

        print("Configuration reload works correctly")

    finally:
        os.remove(temp_path)


def run_all_tests():
    """Run all test functions."""
    tests = [
        test_valid_yaml_config,
        test_minimal_config_with_defaults,
        test_invalid_config_detection,
        test_missing_required_fields,
        test_config_reload,
    ]

    print("Running Configuration Loader Tests")
    print("=" * 50)

    for test in tests:
        try:
            print(f"\nRunning: {test.__name__}")
            test()
            print(f"✓ {test.__name__} PASSED")
        except Exception as error:
            print(f"✗ {test.__name__} FAILED: {error}")
            raise


if __name__ == "__main__":
    run_all_tests()
