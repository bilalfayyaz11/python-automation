import requests
import hmac
import hashlib
import json
from datetime import datetime, UTC

WEBHOOK_URL = "http://localhost:5000/webhook"
SECRET = "your-secret-key-change-this"

def send_webhook(payload, use_valid_signature=True):
    payload_bytes = json.dumps(payload).encode()

    if use_valid_signature:
        signature = hmac.new(
            key=SECRET.encode(),
            msg=payload_bytes,
            digestmod=hashlib.sha256
        ).hexdigest()
    else:
        signature = "invalid_signature"

    headers = {
        "Content-Type": "application/json",
        "X-Hub-Signature-256": f"sha256={signature}"
    }

    response = requests.post(
        WEBHOOK_URL,
        data=payload_bytes,
        headers=headers,
        timeout=10
    )

    print("Status:", response.status_code)
    print("Body:", response.text)

if __name__ == "__main__":
    valid_payload = {
        "event": "user.created",
        "timestamp": datetime.now(UTC).isoformat(),
        "data": {
            "user_id": "12345",
            "username": "testuser",
            "token": "this-should-not-appear-in-logs"
        }
    }

    print("Test 1: Sending valid webhook...")
    send_webhook(valid_payload, use_valid_signature=True)

    print("\nTest 2: Sending webhook with invalid signature...")
    send_webhook(valid_payload, use_valid_signature=False)

    invalid_payload = {
        "wrong_field": "value"
    }

    print("\nTest 3: Sending invalid payload...")
    send_webhook(invalid_payload, use_valid_signature=True)
