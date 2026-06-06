import sys
import json
import uuid
import yaml
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from flask import Flask, request, jsonify
import redis

from policies.policy_engine import PolicyEngine
from workers.task_worker import execute_automation_task


app = Flask(__name__)


def load_config():
    with open(PROJECT_ROOT / "config.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


config = load_config()
redis_cfg = config.get("redis", {})

redis_client = redis.Redis(
    host=redis_cfg.get("host", "localhost"),
    port=int(redis_cfg.get("port", 6379)),
    db=int(redis_cfg.get("db", 0)),
    decode_responses=True
)

policy_engine = PolicyEngine(str(PROJECT_ROOT / "config.yaml"))


def write_api_log(message):
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    with open(log_dir / "api_events.log", "a", encoding="utf-8") as file:
        file.write(f"{datetime.utcnow().isoformat()}Z {message}\n")


@app.route("/health", methods=["GET"])
def health():
    try:
        redis_client.ping()
        redis_status = "connected"
    except Exception:
        redis_status = "unavailable"

    return jsonify({
        "status": "healthy",
        "service": "automation-platform-mvp",
        "redis": redis_status
    })


@app.route("/api/tasks", methods=["POST"])
def create_task():
    try:
        task_data = request.get_json(force=True)
    except Exception:
        return jsonify({"error": "Invalid JSON payload"}), 400

    is_valid, message = policy_engine.validate_task(task_data)
    if not is_valid:
        write_api_log(f"REJECTED reason={message}")
        return jsonify({
            "accepted": False,
            "error": message
        }), 400

    task_id = f"{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8]}"
    task_type = task_data["task_type"]
    parameters = task_data["parameters"]

    celery_result = execute_automation_task.delay(task_id, task_type, parameters)

    metadata = {
        "task_id": task_id,
        "celery_task_id": celery_result.id,
        "task_type": task_type,
        "parameters": parameters,
        "priority": task_data.get("priority", "medium"),
        "status": "queued",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "updated_at": datetime.utcnow().isoformat() + "Z"
    }

    redis_client.setex(f"task:{task_id}", 3600, json.dumps(metadata))
    redis_client.sadd("tasks", task_id)

    write_api_log(f"QUEUED task_id={task_id} type={task_type}")

    return jsonify({
        "accepted": True,
        "task_id": task_id,
        "status": "queued",
        "celery_task_id": celery_result.id
    }), 202


@app.route("/api/tasks/<task_id>", methods=["GET"])
def get_task_status(task_id: str):
    raw = redis_client.get(f"task:{task_id}")

    if not raw:
        return jsonify({"error": "Task not found", "task_id": task_id}), 404

    task_data = json.loads(raw)
    return jsonify(task_data)


@app.route("/api/tasks", methods=["GET"])
def list_tasks():
    status_filter = request.args.get("status")
    type_filter = request.args.get("type")

    task_ids = sorted(redis_client.smembers("tasks"))
    tasks = []

    for task_id in task_ids:
        raw = redis_client.get(f"task:{task_id}")
        if not raw:
            continue

        task = json.loads(raw)

        if status_filter and task.get("status") != status_filter:
            continue

        if type_filter and task.get("task_type") != type_filter:
            continue

        tasks.append(task)

    return jsonify({
        "count": len(tasks),
        "tasks": tasks
    })


def start_api():
    api_cfg = config.get("api", {})
    app.run(
        host=api_cfg.get("host", "0.0.0.0"),
        port=int(api_cfg.get("port", 5000))
    )


if __name__ == "__main__":
    start_api()
