#!/bin/bash

cd ~/automation-platform-mvp

if [ -f logs/api.pid ]; then
  kill "$(cat logs/api.pid)" 2>/dev/null || true
fi

if [ -f logs/worker.pid ]; then
  kill "$(cat logs/worker.pid)" 2>/dev/null || true
fi

pkill -f "api/automation_api.py" 2>/dev/null || true
pkill -f "celery.*workers.task_worker" 2>/dev/null || true

echo "Platform stopped."
