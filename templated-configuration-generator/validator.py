#!/usr/bin/env python3

import sys
import yaml
import json

from jsonschema import validate, ValidationError, SchemaError
from pathlib import Path


class ConfigValidator:
    def __init__(self, schema_dir="schemas"):
        self.schema_dir = schema_dir
        self.schemas = {}

    def load_schema(self, schema_name):
        if schema_name in self.schemas:
            return self.schemas[schema_name]

        schema_path = Path(self.schema_dir) / schema_name

        with open(schema_path, "r", encoding="utf-8") as file:
            schema = json.load(file)

        self.schemas[schema_name] = schema

        return schema

    def validate_yaml_config(self, config_file, schema_name):
        errors = []

        try:
            with open(config_file, "r", encoding="utf-8") as file:
                config = yaml.safe_load(file)

            schema = self.load_schema(schema_name)

            validate(
                instance=config,
                schema=schema
            )

            return True, []

        except FileNotFoundError as error:
            errors.append(str(error))

        except yaml.YAMLError as error:
            errors.append(f"YAML parsing error: {error}")

        except ValidationError as error:
            errors.append(f"Schema validation error: {error.message}")

        except SchemaError as error:
            errors.append(f"Invalid schema: {error.message}")

        except Exception as error:
            errors.append(str(error))

        return False, errors

    def validate_nginx_config(self, config_file):
        try:
            content = Path(config_file).read_text(
                encoding="utf-8"
            )

            if content.count("{") != content.count("}"):
                return False, "Unbalanced curly braces"

            if "server {" not in content:
                return False, "Missing server block"

            if "location /" not in content:
                return False, "Missing location block"

            if "proxy_pass" not in content:
                return False, "Missing proxy_pass directive"

            for line_number, line in enumerate(
                content.splitlines(),
                start=1
            ):
                stripped = line.strip()

                if (
                    not stripped
                    or stripped.startswith("#")
                    or stripped.endswith("{")
                    or stripped.endswith("}")
                ):
                    continue

                if not stripped.endswith(";"):
                    return False, f"Line {line_number} missing semicolon: {stripped}"

            return True, "Nginx configuration structure looks valid"

        except Exception as error:
            return False, str(error)


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 validator.py <config_file> <schema_name>")
        print("Example: python3 validator.py configs/app_config.yaml app_config_schema.json")
        print("Example: python3 validator.py configs/nginx.conf nginx")
        sys.exit(1)

    config_file = sys.argv[1]
    schema_name = sys.argv[2]

    validator = ConfigValidator()

    if schema_name == "nginx":
        is_valid, message = validator.validate_nginx_config(
            config_file
        )

        if is_valid:
            print(f"[PASS] {config_file}: {message}")
            sys.exit(0)

        print(f"[FAIL] {config_file}: {message}")
        sys.exit(1)

    is_valid, errors = validator.validate_yaml_config(
        config_file,
        schema_name
    )

    if is_valid:
        print(f"[PASS] {config_file} passed validation against {schema_name}")
        sys.exit(0)

    print(f"[FAIL] {config_file} failed validation against {schema_name}")

    for error in errors:
        print(f"- {error}")

    sys.exit(1)


if __name__ == "__main__":
    main()
