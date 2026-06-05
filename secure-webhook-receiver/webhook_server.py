from flask import Flask, request, jsonify
import hmac
import hashlib
import json
import logging
from datetime import datetime, UTC
from jsonschema import validate, ValidationError

app = Flask(__name__)

WEBHOOK_SECRET = "your-secret-key-change-this"
LOG_FILE = "webhook_events.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

SENSITIVE_KEYS = {"password", "token", "api_key", "secret", "authorization"}

def utc_timestamp():
    return datetime.now(UTC).isoformat()

def sanitize_payload(payload):
    if isinstance(payload, dict):
        sanitized = {}
        for key, value in payload.items():
            if key.lower() in SENSITIVE_KEYS:
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = sanitize_payload(value)
            elif isinstance(value, list):
                sanitized[key] = [
                    sanitize_payload(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                sanitized[key] = value
        return sanitized
    return payload

def verify_signature(payload_body, signature_header):
    if not signature_header:
        return False

    expected_signature = hmac.new(
        key=WEBHOOK_SECRET.encode(),
        msg=payload_body,
        digestmod=hashlib.sha256
    ).hexdigest()

    expected_header = f"sha256={expected_signature}"

    return hmac.compare_digest(expected_header, signature_header)

def validate_payload(payload):
    schema = {
        "type": "object",
        "properties": {
            "event": {"type": "string", "minLength": 1},
            "timestamp": {"type": "string", "minLength": 1},
            "data": {"type": "object"}
        },
        "required": ["event", "timestamp", "data"],
        "additionalProperties": True
    }

    try:
        validate(instance=payload, schema=schema)
        return True
    except ValidationError as error:
        logging.error(
            json.dumps({
                "timestamp": utc_timestamp(),
                "status": "validation_failed",
                "error": error.message
            })
        )
        return False

def log_webhook_event(event_type, payload, status):
    safe_payload = sanitize_payload(payload)

    log_entry = {
        "timestamp": utc_timestamp(),
        "event_type": event_type,
        "status": status,
        "payload_summary": safe_payload
    }

    logging.info(json.dumps(log_entry))

@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature_header = request.headers.get("X-Hub-Signature-256")
    payload_body = request.get_data()

    if not verify_signature(payload_body, signature_header):
        logging.warning(
            json.dumps({
                "timestamp": utc_timestamp(),
                "status": "signature_verification_failed"
            })
        )
        return jsonify({"error": "invalid signature"}), 401

    try:
        payload = request.get_json(force=True)
    except Exception:
        logging.error(
            json.dumps({
                "timestamp": utc_timestamp(),
                "status": "invalid_json"
            })
        )
        return jsonify({"error": "invalid json"}), 400

    if not validate_payload(payload):
        return jsonify({"error": "invalid payload"}), 400

    event_type = payload.get("event", "unknown")
    log_webhook_event(event_type, payload, "success")

    return jsonify({
        "message": "webhook received",
        "event": event_type,
        "status": "processed"
    }), 200

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
