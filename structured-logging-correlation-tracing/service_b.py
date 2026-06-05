from flask import Flask, request, jsonify, g
import logging
from pythonjsonlogger import jsonlogger
import time

app = Flask(__name__)

def setup_logging():

    logger = logging.getLogger("service_b")
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
        "missing"
    )

@app.route('/api/inventory/check', methods=['POST'])
def check_inventory():

    data = request.get_json()

    logger.info(
        "inventory request",
        extra={
            "correlation_id": g.correlation_id
        }
    )

    time.sleep(0.05)

    result = {
        "product_id": data.get("product_id"),
        "available": True,
        "quantity": 50
    }

    logger.info(
        "inventory response",
        extra={
            "correlation_id": g.correlation_id
        }
    )

    return jsonify(result)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )
