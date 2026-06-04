import redis
import json
import time
import random
import sys

sys.path.append('/app')

from shared.config import Config

def get_redis_client():
    return redis.Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        decode_responses=True
    )

def process_task(task_data):

    task_type = task_data["task_type"]

    data = task_data["data"]

    time.sleep(random.randint(2,5))

    return {
        "task_type": task_type,
        "input": data,
        "status": "completed",
        "processed_at": time.time()
    }

def main():

    print("Worker starting...")

    r = get_redis_client()

    while True:

        try:

            queue_item = r.blpop("task_queue", timeout=5)

            if not queue_item:
                continue

            _, task_json = queue_item

            task = json.loads(task_json)

            task_id = task["task_id"]

            result = process_task(task)

            r.set(
                f"result:{task_id}",
                json.dumps(result)
            )

            print(f"Processed task {task_id}")

        except KeyboardInterrupt:
            print("Worker shutting down...")
            break

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()
