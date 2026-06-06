#!/usr/bin/env python3

import subprocess
import requests
import time
import yaml
import sys


class DeploymentGate:
    def __init__(self, config_path):
        with open(config_path, "r") as file:
            self.config = yaml.safe_load(file)["deployment"]

        self.app_name = self.config["app_name"]
        self.port = self.config["port"]
        self.candidate_name = f"{self.app_name}-candidate"
        self.previous_name = f"{self.app_name}-previous"

    def run_command(self, command):
        return subprocess.run(command, capture_output=True, text=True)

    def container_exists(self, name):
        result = self.run_command(["docker", "ps", "-a", "--format", "{{.Names}}"])
        return name in result.stdout.splitlines()

    def remove_container(self, name):
        self.run_command(["docker", "rm", "-f", name])

    def start_candidate(self, version):
        print(f"Starting candidate version {version} on port 5001")

        self.remove_container(self.candidate_name)

        result = self.run_command([
            "docker", "run", "-d",
            "--name", self.candidate_name,
            "-p", "5001:5000",
            "-e", f"APP_VERSION={version}",
            f"{self.app_name}:{version}"
        ])

        if result.returncode != 0:
            print(result.stderr)
            return False

        return True

    def check_endpoint(self, endpoint_config, port):
        endpoint = f"http://localhost:{port}{endpoint_config['endpoint']}"

        for attempt in range(1, endpoint_config["retries"] + 1):
            try:
                response = requests.get(endpoint, timeout=endpoint_config["timeout"])

                if response.status_code == 200:
                    print(f"PASS: {endpoint}")
                    return True

                print(f"FAIL attempt {attempt}: HTTP {response.status_code}")

            except Exception as error:
                print(f"FAIL attempt {attempt}: {error}")

            time.sleep(endpoint_config["interval"])

        return False

    def health_check_candidate(self):
        return self.check_endpoint(self.config["health_check"], 5001)

    def readiness_check_candidate(self):
        return self.check_endpoint(self.config["readiness_check"], 5001)

    def promote_candidate(self):
        print("Promoting candidate to production")

        if self.container_exists(self.previous_name):
            self.remove_container(self.previous_name)

        if self.container_exists(self.app_name):
            self.run_command(["docker", "stop", self.app_name])
            self.run_command(["docker", "rename", self.app_name, self.previous_name])

        self.run_command(["docker", "stop", self.candidate_name])
        self.remove_container(self.candidate_name)

        result = self.run_command([
            "docker", "run", "-d",
            "--name", self.app_name,
            "-p", "5000:5000",
            f"{self.app_name}:{self.version}"
        ])

        if result.returncode != 0:
            print(result.stderr)
            self.rollback()
            return False

        time.sleep(5)

        if not self.check_endpoint(self.config["health_check"], 5000):
            self.rollback()
            return False

        print("Production promotion successful")
        return True

    def rollback(self):
        print("ROLLBACK TRIGGERED")

        if self.container_exists(self.candidate_name):
            self.remove_container(self.candidate_name)

        if self.container_exists(self.app_name):
            self.remove_container(self.app_name)

        if self.container_exists(self.previous_name):
            self.run_command(["docker", "rename", self.previous_name, self.app_name])
            self.run_command(["docker", "start", self.app_name])
            print("Rollback completed")
            return True

        print("No previous stable container available")
        return False

    def deploy(self, version):
        self.version = version

        print("=" * 60)
        print(f"DEPLOYMENT STARTED: {version}")
        print("=" * 60)

        if not self.start_candidate(version):
            return False

        time.sleep(5)

        print("GATE 1: Candidate Health Check")
        if not self.health_check_candidate():
            self.rollback()
            return False

        print("GATE 2: Candidate Readiness Check")
        if not self.readiness_check_candidate():
            self.rollback()
            return False

        if not self.promote_candidate():
            return False

        print("=" * 60)
        print("DEPLOYMENT SUCCESSFUL")
        print("=" * 60)

        return True


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 deploy_with_gate.py <version>")
        sys.exit(1)

    gate = DeploymentGate("config/deployment.yaml")
    success = gate.deploy(sys.argv[1])

    sys.exit(0 if success else 1)
