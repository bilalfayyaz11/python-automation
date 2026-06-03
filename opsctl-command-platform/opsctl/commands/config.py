"""Configuration command implementation."""

import json
import os
from opsctl.utils.helpers import print_success, print_error, print_info


CONFIG_FILE = os.path.expanduser("~/.opsctl/config.json")


def _load_config():
    if not os.path.exists(CONFIG_FILE):
        return {}

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print_error("Configuration file is corrupted or invalid JSON")
        return {}


def _save_config(config_data):
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config_data, file, indent=2)


def execute(args):
    """Execute the config command."""
    config_data = _load_config()

    if args.action == "get":
        if args.key not in config_data:
            print_error(f"Configuration key not found: {args.key}")
            return 1

        print(config_data[args.key])
        return 0

    if args.action == "set":
        config_data[args.key] = args.value
        _save_config(config_data)
        print_success(f"Configuration saved: {args.key}")
        return 0

    print_error("Unsupported config action")
    return 2


def add_parser(subparsers):
    """Add config command parser."""
    parser = subparsers.add_parser(
        "config",
        help="Get or set CLI configuration values",
        description="Manage persistent opsctl configuration values",
    )

    action_parsers = parser.add_subparsers(
        dest="action",
        help="Configuration action",
        required=True,
    )

    get_parser = action_parsers.add_parser("get", help="Get a configuration value")
    get_parser.add_argument("key", help="Configuration key to retrieve")
    get_parser.set_defaults(func=execute)

    set_parser = action_parsers.add_parser("set", help="Set a configuration value")
    set_parser.add_argument("key", help="Configuration key to store")
    set_parser.add_argument("value", help="Configuration value to store")
    set_parser.set_defaults(func=execute)
