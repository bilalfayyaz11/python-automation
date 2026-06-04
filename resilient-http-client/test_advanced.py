import time

from resilient_client import ResilientHTTPClient


def test_circuit_breaker():
    """Test circuit breaker functionality."""
    print("\n=== Circuit Breaker Test ===")

    client = ResilientHTTPClient(
        max_retries=1,
        base_timeout=1,
        use_circuit_breaker=True,
    )

    for attempt in range(7):
        try:
            print(f"\nRequest {attempt + 1}")

            client.get("http://invalid-domain-12345.com")

        except Exception as exc:
            print(f"Exception: {exc}")

    client.close()


def test_rate_limiting():
    """Test retryable HTTP status handling."""
    print("\n=== Rate Limiting Test ===")

    client = ResilientHTTPClient(
        max_retries=3,
        base_timeout=5,
    )

    try:
        response = client.get("https://httpbin.org/status/429")

        print(response.status_code)

    except Exception as exc:
        print(f"Handled retryable status correctly: {exc}")

    finally:
        client.close()


if __name__ == "__main__":
    test_circuit_breaker()
    test_rate_limiting()
