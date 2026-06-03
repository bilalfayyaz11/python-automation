"""Practical usage example for the typed configuration loader."""

import sys

from config_loader import ConfigLoader


def main():
    """Load a configuration file and print a readable summary."""
    if len(sys.argv) < 2:
        print("Usage: python3 app_example.py <config_file>")
        sys.exit(1)

    config_path = sys.argv[1]

    try:
        loader = ConfigLoader(config_path)
        config = loader.load()

        print("Configuration loaded successfully")
        print("=" * 50)
        print(f"Application: {config.app_name}")
        print(f"Environment: {config.environment}")
        print(f"Debug Mode: {config.debug}")
        print()
        print("Database")
        print("-" * 50)
        print(f"Host: {config.database.host}")
        print(f"Port: {config.database.port}")
        print(f"Database: {config.database.database}")
        print(f"Username: {config.database.username}")
        print(f"Max Connections: {config.database.max_connections}")
        print()
        print("Cache")
        print("-" * 50)
        print(f"Enabled: {config.cache.enabled}")
        print(f"TTL Seconds: {config.cache.ttl_seconds}")
        print(f"Max Size MB: {config.cache.max_size_mb}")
        print()
        print("Logging")
        print("-" * 50)
        print(f"Level: {config.logging.level}")
        print(f"Format: {config.logging.format}")
        print(f"Output Path: {config.logging.output_path}")

    except Exception as error:
        print(f"Failed to load configuration: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
