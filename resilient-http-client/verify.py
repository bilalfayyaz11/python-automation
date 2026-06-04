from resilient_client import ResilientHTTPClient


client = ResilientHTTPClient(
    max_retries=3,
    base_timeout=2,
)

print("Backoff delays:")

for i in range(4):
    delay = client._calculate_backoff(i)
    print(f"Attempt {i}: {delay}s")

try:
    response = client.get("https://httpbin.org/status/200")
    print(f"\nSuccess test: Status {response.status_code}")

except Exception as exc:
    print(f"Failed: {exc}")

finally:
    client.close()
