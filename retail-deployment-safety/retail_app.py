from flask import Flask, jsonify
import time
import os

app = Flask(__name__)

app_state = {
    "version": os.getenv("APP_VERSION", "1.0.0"),
    "start_time": time.time(),
    "healthy": True,
    "ready": True
}

@app.route("/")
def home():
    return jsonify({
        "service": "Retail API",
        "version": app_state["version"],
        "status": "running"
    })

@app.route("/health")
def health():
    if not app_state["healthy"]:
        return jsonify({
            "status": "unhealthy",
            "version": app_state["version"]
        }), 503

    return jsonify({
        "status": "healthy",
        "version": app_state["version"]
    }), 200

@app.route("/ready")
def ready():
    uptime = time.time() - app_state["start_time"]

    if uptime < 5:
        return jsonify({
            "status": "warming_up",
            "uptime": round(uptime, 2)
        }), 503

    if not app_state["ready"]:
        return jsonify({
            "status": "not_ready",
            "version": app_state["version"]
        }), 503

    return jsonify({
        "status": "ready",
        "version": app_state["version"],
        "uptime": round(uptime, 2)
    }), 200

@app.route("/products")
def products():
    return jsonify({
        "products": [
            {"id": 1, "name": "Laptop", "price": 999.99},
            {"id": 2, "name": "Mouse", "price": 29.99},
            {"id": 3, "name": "Keyboard", "price": 79.99}
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
