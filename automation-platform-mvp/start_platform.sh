#!/bin/bash
set -e

cd ~/automation-platform-mvp
source venv/bin/activate

mkdir -p logs

if pgrep -f "api/automation_api.py" >/dev/null; then
  pkill -f "api/automation_api.py" || true
fi

if pgrep -f "celery.*workers.task_worker" >/dev/null; then
  pkill -f "celery.*workers.task_worker" || true
fi

python3 api/automation_api.py > logs/api.log 2>&1 &
API_PID=$!
echo "$API_PID" > logs/api.pid
echo "API started with PID: $API_PID"

celery -A workers.task_worker worker --loglevel=info --concurrency=2 > logs/celery.log 2>&1 &
WORKER_PID=$!
echo "$WORKER_PID" > logs/worker.pid
echo "Worker started with PID: $WORKER_PID"

sleep 3

echo "Platform started."
echo "API log: logs/api.log"
echo "Worker log: logs/celery.log"
