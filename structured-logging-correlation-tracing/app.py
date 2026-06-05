from flask import Flask, request, jsonify, g
import logging
from pythonjsonlogger import jsonlogger
import uuid
import time
import requests

app = Flask(__name__)

def setup_logging():
    logger = logging.getLogger()
    logger.handlers.clear()

    handler = logging.StreamHandler()

    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(correlation_id)s %(message)s'
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    return logger

logger = setup_logging()

@app.before_request
def before_request():
    g.correlation_id = request.headers.get(
        "X-Correlation-ID",
        str(uuid.uuid4())
    )

def log_with_context(level, message, **kwargs):

    extra = {
        "correlation_id": getattr(g, "correlation_id", "unknown")
    }

    extra.update(kwargs)

    if level == "info":
        logger.info(message, extra=extra)

    elif level == "warning":
        logger.warning(message, extra=extra)

    elif level == "error":
        logger.error(message, extra=extra)

@app.route('/api/users', methods=['GET'])
def get_users():

    log_with_context(
        "info",
        "users endpoint called"
    )

    time.sleep(0.1)

    users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"}
    ]

    log_with_context(
        "info",
        "users returned",
        count=len(users)
    )

    return jsonify(users)

@app.route('/api/orders', methods=['POST'])
def create_order():

    data = request.get_json()

    if not data:
        log_with_context(
            "error",
            "invalid request body"
        )
        return jsonify({"error": "invalid body"}), 400

    order = {
        "order_id": str(uuid.uuid4()),
        "user_id": data.get("user_id"),
        "amount": data.get("amount")
    }

    log_with_context(
        "info",
        "order created",
        order_id=order["order_id"]
    )

    return jsonify(order), 201

@app.route('/api/orders/full', methods=['POST'])
def create_full_order():

    data = request.get_json()

    log_with_context(
        "info",
        "starting full order workflow"
    )

    headers = {
        "X-Correlation-ID": g.correlation_id,
        "Content-Type": "application/json"
    }

    inventory_response = requests.post(
        "http://localhost:5001/api/inventory/check",
        json={
            "product_id": data.get("product_id")
        },
        headers=headers,
        timeout=5
    )

    inventory = inventory_response.json()

    log_with_context(
        "info",
        "inventory checked",
        available=inventory["available"]
    )

    order = {
        "order_id": str(uuid.uuid4()),
        "product_id": data.get("product_id"),
        "status": "confirmed"
    }

    log_with_context(
        "info",
        "order workflow completed",
        order_id=order["order_id"]
    )

    return jsonify(order), 201

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
