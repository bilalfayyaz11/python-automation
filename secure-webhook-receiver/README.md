
# Secure Webhook Receiver

## What This Does

This implementation provides a secure webhook receiver that validates incoming webhook requests before processing them.

The application verifies HMAC-SHA256 signatures, validates JSON payload structures using schemas, sanitizes sensitive information before logging, and records structured audit events. The implementation demonstrates production-grade webhook security patterns commonly used by GitHub, GitLab, Stripe, PayPal, PagerDuty, Datadog, and similar event-driven platforms.

## Architecture

```
External Service
        |
        | HTTP POST + JSON Payload
        | X-Hub-Signature-256 Header
        v
+----------------------------+
| Flask Webhook Receiver     |
+----------------------------+
             |
             v
+----------------------------+
| Signature Verification     |
| HMAC-SHA256                |
| compare_digest()           |
+----------------------------+
             |
             v
+----------------------------+
| JSON Schema Validation     |
+----------------------------+
             |
             v
+----------------------------+
| Secure Logging Layer       |
| Sensitive Data Redaction   |
+----------------------------+
             |
             v
webhook_events.log
```

## Prerequisites

* Ubuntu 24.04
* Python 3
* Python pip
* Python virtual environments
* Flask
* jsonschema
* requests

## Setup & Installation

Install dependencies:

sudo apt update

sudo apt install -y 
python3 
python3-pip 
python3-venv

Create environment:

python3 -m venv venv

source venv/bin/activate

Install packages:

pip install --upgrade pip

pip install flask jsonschema requests

## How to Reproduce

Start the server:

source venv/bin/activate

python3 webhook_server.py

Verify health endpoint:

curl http://localhost:5000/health

Expected response:

{"status":"healthy"}

Run webhook tests:

python3 test_webhook.py

Expected Results:

* Valid webhook returns HTTP 200
* Invalid signature returns HTTP 401
* Invalid payload returns HTTP 400

Verify logs:

cat webhook_events.log

Verify sensitive data redaction:

grep -i token webhook_events.log

Sensitive values should appear as:

[REDACTED]

## Tools Used

* Python 3
* Flask
* jsonschema
* requests
* HMAC
* SHA256
* Linux
* Bash
* curl

## Key Skills Demonstrated

* Secure webhook processing
* HMAC signature verification
* Constant-time signature comparison
* JSON schema validation
* Secure event logging
* Secret redaction
* Flask API development
* HTTP security controls
* DevSecOps best practices
* Defensive programming

## Real-World Use Case

Webhook receivers are used throughout modern cloud-native systems. GitHub sends repository events, Stripe sends payment events, PagerDuty sends incident notifications, and monitoring platforms send alerts through webhooks.

Production systems must verify that these requests originate from trusted sources before taking action. Signature verification, payload validation, and secure logging form the foundation of secure webhook processing in enterprise environments.

## Lessons Learned

* Never trust external webhook payloads without verification.
* HMAC signatures protect against forged requests.
* Constant-time comparison prevents timing attacks.
* Schema validation prevents malformed data processing.
* Sensitive information should never be written to logs.
* Security validation must happen before business logic execution.

## Troubleshooting Log

Issue:
Webhook signatures failed validation.

Resolution:
Used request.get_data() to obtain raw request bytes before JSON parsing.

Issue:
Timing attack risk during signature comparison.

Resolution:
Implemented hmac.compare_digest() for constant-time comparison.

Issue:
Sensitive information appearing in logs.

Resolution:
Added sanitization logic for token, password, secret, api_key, and authorization fields.

Issue:
Invalid payload structures caused processing failures.

Resolution:
Implemented JSON Schema validation and explicit HTTP 400 responses.

Issue:
Test client dependency missing.

Resolution:
Added requests package to installation requirements.
