from resilient_client import ResilientHTTPClient


def test_successful_request():
    """Test basic successful request."""
    print("\n=== Test 1: Successful Request ===")

    client = ResilientHTTPClient(max_retries=3, base_timeout=10)

    try:
        response = client.get("https://httpbin.org/get")

        print(f"Status Code: {response.status_code}")
        print(f"URL: {response.json()['url']}")

    except Exception as exc:
        print(f"Error: {exc}")

    finally:
        client.close()


def test_timeout_handling():
    """Test timeout with retry."""
    print("\n=== Test 2: Timeout Handling ===")

    client = ResilientHTTPClient(
        max_retries=3,
        base_timeout=1,
    )

    try:
        client.get("https://httpbin.org/delay/5")

    except Exception as exc:
        print(f"Final Exception: {exc}")

    finally:
        client.close()


def test_retry_on_failure():
    """Test retry on connection failure."""
    print("\n=== Test 3: Retry on Failure ===")

    client = ResilientHTTPClient(
        max_retries=3,
        base_timeout=3,
    )

    try:
        client.get("http://invalid-domain-12345.com")

    except Exception as exc:
        print(f"Final Exception: {exc}")

    finally:
        client.close()


def test_post_request():
    """Test POST request with data."""
    print("\n=== Test 4: POST Request ===")

    client = ResilientHTTPClient()

    try:
        response = client.post(
            "https://httpbin.org/post",
            json={
                "application": "resilient-http-client",
                "status": "success",
            },
        )

        print(f"Status Code: {response.status_code}")
        print(response.json()["json"])

    except Exception as exc:
        print(f"Error: {exc}")

    finally:
        client.close()


if __name__ == "__main__":
    test_successful_request()
    test_timeout_handling()
    test_retry_on_failure()
    test_post_request()
