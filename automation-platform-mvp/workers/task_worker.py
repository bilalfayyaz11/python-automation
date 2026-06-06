import sys
import time
import json
import yaml
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from celery import Celery
import redis


def load_config():
    with open(PROJECT_ROOT / "config.yaml", "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


config = load_config()
redis_cfg = config.get("redis", {})
redis_host = redis_cfg.get("host", "localhost")
redis_port = int(redis_cfg.get("port", 6379))
redis_db = int(redis_cfg.get("db", 0))

broker_url = f"redis://{redis_host}:{redis_port}/{redis_db}"
result_backend = f"redis://{redis_host}:{redis_port}/{redis_db}"

app = Celery("automation_platform", broker=broker_url, backend=result_backend)

app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
    task_track_started=True
)

redis_client = redis.Redis(host=redis_host, port=redis_port, db=redis_db, decode_responses=True)


def write_worker_log(message):
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(exist_ok=True)
    with open(log_dir / "worker_events.log", "a", encoding="utf-8") as file:
        file.write(f"{datetime.utcnow().isoformat()}Z {message}\n")


def update_task_status(task_id, status, result=None, error=None):
    key = f"task:{task_id}"
    raw = redis_client.get(key)

    task_data = json.loads(raw) if raw else {"task_id": task_id}
    task_data["status"] = status
    task_data["updated_at"] = datetime.utcnow().isoformat() + "Z"

    if result is not None:
        task_data["result"] = result

    if error is not None:
        task_data["error"] = error

    redis_client.setex(key, 3600, json.dumps(task_data))


@app.task(bind=True, max_retries=3, name="workers.task_worker.execute_automation_task")
def execute_automation_task(self, task_id: str, task_type: str, parameters: dict):
    try:
        write_worker_log(f"START task_id={task_id} type={task_type}")
        update_task_status(task_id, "running")

        time.sleep(2)

        if task_type == "backup":
            result = {
                "operation": "backup",
                "source": parameters.get("path"),
                "destination": parameters.get("destination"),
                "message": "Backup simulation completed"
            }

        elif task_type == "deploy":
            result = {
                "operation": "deploy",
                "service": parameters.get("service"),
                "version": parameters.get("version"),
                "message": "Deployment simulation completed"
            }

        elif task_type == "cleanup":
            result = {
                "operation": "cleanup",
                "target": parameters.get("target"),
                "message": "Cleanup simulation completed"
            }

        else:
            raise ValueError(f"Unsupported task type: {task_type}")

        update_task_status(task_id, "completed", result=result)
        write_worker_log(f"SUCCESS task_id={task_id} type={task_type}")

        return {
            "task_id": task_id,
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat() + "Z",
            "result": result
        }

    except Exception as exc:
        write_worker_log(f"ERROR task_id={task_id} error={str(exc)}")
        update_task_status(task_id, "retrying", error=str(exc))

        try:
            raise self.retry(exc=exc, countdown=5)
        except self.MaxRetriesExceededError:
            update_task_status(task_id, "failed", error=str(exc))
            write_worker_log(f"FAILED task_id={task_id} error={str(exc)}")
            raise


def start_worker():
    app.worker_main([
        "worker",
        "--loglevel=info",
        f"--concurrency={config.get('workers', {}).get('concurrency', 2)}"
    ])
