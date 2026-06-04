from flask import Flask, jsonify, request
import redis
import json
import uuid
import sys

sys.path.append('/app')

from shared.config import Config

app = Flask(__name__)

def get_redis_client():
    return redis.Redis(
        host=Config.REDIS_HOST,
        port=Config.REDIS_PORT,
        decode_responses=True
    )

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.route('/task', methods=['POST'])
def create_task():

    task_data = request.get_json()

    task_id = str(uuid.uuid4())

    payload = {
        "task_id": task_id,
        "task_type": task_data.get("task_type"),
        "data": task_data.get("data", {})
    }

    r = get_redis_client()

    r.rpush("task_queue", json.dumps(payload))

    return jsonify({
        "status": "queued",
        "task_id": task_id
    }), 202

@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):

    r = get_redis_client()

    result = r.get(f"result:{task_id}")

    if not result:
        return jsonify({"error": "Result not found"}), 404

    return jsonify(json.loads(result)), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=Config.API_PORT)
