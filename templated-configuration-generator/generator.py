#!/usr/bin/env python3

import os
import sys
import yaml

from pathlib import Path
from jinja2 import Environment, FileSystemLoader, TemplateNotFound


class ConfigGenerator:
    def __init__(self, template_dir="templates", output_dir="configs"):
        self.template_dir = template_dir
        self.output_dir = output_dir

        self.env = Environment(
            loader=FileSystemLoader(self.template_dir),
            trim_blocks=True,
            lstrip_blocks=True
        )

        Path(self.output_dir).mkdir(
            parents=True,
            exist_ok=True
        )

    def load_data(self, data_file):
        try:
            with open(data_file, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file)

            if not isinstance(data, dict):
                raise ValueError("Configuration data must be a YAML mapping")

            return data

        except FileNotFoundError:
            raise FileNotFoundError(f"Data file not found: {data_file}")

        except yaml.YAMLError as error:
            raise ValueError(f"Invalid YAML in {data_file}: {error}")

    def generate_config(self, template_name, data, output_file=None):
        try:
            template = self.env.get_template(template_name)

        except TemplateNotFound:
            raise FileNotFoundError(f"Template not found: {template_name}")

        rendered_config = template.render(**data)

        if output_file is None:
            output_file = template_name.replace(".j2", "")

        output_path = Path(self.output_dir) / output_file

        with open(output_path, "w", encoding="utf-8") as file:
            file.write(rendered_config)

        print(f"Generated: {output_path}")

        return rendered_config

    def generate_all(self, data_file, template_list=None):
        data = self.load_data(data_file)

        if template_list is None:
            template_list = [
                template
                for template in os.listdir(self.template_dir)
                if template.endswith(".j2")
            ]

        generated_files = []

        for template_name in template_list:
            output_file = template_name.replace(".j2", "")
            self.generate_config(
                template_name,
                data,
                output_file
            )
            generated_files.append(output_file)

        print("\nGeneration Summary")
        print("=" * 50)

        for file_name in generated_files:
            print(f"- {self.output_dir}/{file_name}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 generator.py <data_file> [template1 template2 ...]")
        print("Example: python3 generator.py data/dev_config.yaml")
        sys.exit(1)

    data_file = sys.argv[1]
    templates = sys.argv[2:] if len(sys.argv) > 2 else None

    generator = ConfigGenerator()
    generator.generate_all(data_file, templates)


if __name__ == "__main__":
    main()
