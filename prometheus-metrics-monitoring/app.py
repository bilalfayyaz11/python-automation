from flask import Flask, Response, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest, REGISTRY
import time
import random

app = Flask(__name__)

http_requests = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"]
)

request_duration = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "endpoint"]
)

active_connections = Gauge(
    "active_connections",
    "Number of active connections"
)

system_health_score = Gauge(
    "system_health_score",
    "Current system health score"
)

@app.route("/")
def home():
    active_connections.inc()
    start_time = time.time()

    try:
        time.sleep(random.uniform(0.1, 0.5))
        duration = time.time() - start_time

        request_duration.labels("GET", "/").observe(duration)
        http_requests.labels("GET", "/", "200").inc()

        return "Hello from Instrumented App!"

    finally:
        active_connections.dec()

@app.route("/api/data")
def api_data():
    active_connections.inc()
    start_time = time.time()

    try:
        time.sleep(random.uniform(0.2, 0.8))
        duration = time.time() - start_time

        request_duration.labels("GET", "/api/data").observe(duration)
        http_requests.labels("GET", "/api/data", "200").inc()

        return jsonify({
            "status": "success",
            "data": [1, 2, 3, 4, 5]
        })

    finally:
        active_connections.dec()

@app.route("/health")
def health():
    score = random.randint(50, 100)
    system_health_score.set(score)

    http_requests.labels("GET", "/health", "200").inc()

    return jsonify({
        "health": "ok",
        "score": score
    })

@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(REGISTRY),
        mimetype="text/plain"
    )

if __name__ == "__main__":
    system_health_score.set(100)
    app.run(host="0.0.0.0", port=8000)
