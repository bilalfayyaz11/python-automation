#!/usr/bin/env python3
import requests
import json


class PolicyGateClient:
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url

    def switch_profile(self, profile_name: str) -> dict:
        response = requests.post(
            f"{self.base_url}/switch-profile",
            json={"profile": profile_name},
            timeout=5
        )
        return response.json()

    def enforce_request(self, request_data: dict) -> dict:
        response = requests.post(
            f"{self.base_url}/enforce",
            json=request_data,
            timeout=5
        )
        return response.json()

    def get_status(self) -> dict:
        response = requests.get(f"{self.base_url}/status", timeout=5)
        return response.json()

    def get_profiles(self) -> dict:
        response = requests.get(f"{self.base_url}/profiles", timeout=5)
        return response.json()


def print_result(title, result):
    print(f"\n===== {title} =====")
    print(json.dumps(result, indent=2))


def test_healthcare_profile(client):
    print_result("Switch Healthcare", client.switch_profile("healthcare"))

    non_compliant = {
        "data_type": "PHI",
        "encrypted": False,
        "access_logged": True,
        "retention_days": 1200
    }

    compliant = {
        "data_type": "PHI",
        "encrypted": True,
        "access_logged": True,
        "retention_days": 1200
    }

    print_result("Healthcare Non-Compliant", client.enforce_request(non_compliant))
    print_result("Healthcare Compliant", client.enforce_request(compliant))


def test_finance_profile(client):
    print_result("Switch Finance", client.switch_profile("finance"))

    non_compliant = {
        "data_type": "cardholder_data",
        "encrypted": True,
        "network_segmented": False,
        "password_length": 8
    }

    compliant = {
        "data_type": "cardholder_data",
        "encrypted": True,
        "network_segmented": True,
        "password_length": 14
    }

    print_result("Finance Non-Compliant", client.enforce_request(non_compliant))
    print_result("Finance Compliant", client.enforce_request(compliant))


def test_retail_profile(client):
    print_result("Switch Retail", client.switch_profile("retail"))

    non_compliant = {
        "data_type": "customer_pii",
        "encrypted": False,
        "request_count": 1500
    }

    compliant = {
        "data_type": "customer_pii",
        "encrypted": True,
        "request_count": 250
    }

    print_result("Retail Non-Compliant", client.enforce_request(non_compliant))
    print_result("Retail Compliant", client.enforce_request(compliant))


def main():
    client = PolicyGateClient()

    print_result("Profiles", client.get_profiles())
    print_result("Status", client.get_status())

    test_healthcare_profile(client)
    test_finance_profile(client)
    test_retail_profile(client)


if __name__ == "__main__":
    main()
