#!/bin/bash
set -e

cd ~/automation-platform-mvp
source venv/bin/activate

echo "===== REDIS ====="
redis-cli ping

echo
echo "===== API HEALTH ====="
curl -s http://localhost:5000/health | jq

echo
echo "===== POLICY REJECTION TEST ====="
curl -s -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type": "invalid", "parameters": {}}' | jq

echo
echo "===== SUBMIT BACKUP TASK ====="
BACKUP_RESPONSE=$(curl -s -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type": "backup", "parameters": {"path": "/data", "destination": "/backup"}, "priority": "high"}')

echo "$BACKUP_RESPONSE" | jq
BACKUP_ID=$(echo "$BACKUP_RESPONSE" | jq -r '.task_id')

echo
echo "===== SUBMIT DEPLOY TASK ====="
DEPLOY_RESPONSE=$(curl -s -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"task_type": "deploy", "parameters": {"service": "web-app", "version": "1.2.3"}, "priority": "high"}')

echo "$DEPLOY_RESPONSE" | jq
DEPLOY_ID=$(echo "$DEPLOY_RESPONSE" | jq -r '.task_id')

echo
echo "===== SUBMIT CLEANUP TASKS WITH CLI ====="
for i in {1..3}; do
  python3 cli/automation_cli.py submit \
    --type cleanup \
    --params "{\"target\": \"temp-$i\"}" \
    --priority low
done

sleep 8

echo
echo "===== BACKUP TASK STATUS ====="
curl -s "http://localhost:5000/api/tasks/$BACKUP_ID" | jq

echo
echo "===== DEPLOY TASK STATUS ====="
curl -s "http://localhost:5000/api/tasks/$DEPLOY_ID" | jq

echo
echo "===== LIST ALL TASKS ====="
curl -s http://localhost:5000/api/tasks | jq

echo
echo "===== LIST COMPLETED TASKS VIA CLI ====="
python3 cli/automation_cli.py list --status completed

echo
echo "===== REDIS TASK KEYS ====="
redis-cli KEYS "task:*"

echo
echo "===== API LOG TAIL ====="
tail -20 logs/api.log

echo
echo "===== CELERY LOG TAIL ====="
tail -40 logs/celery.log

echo
echo "===== WORKER EVENT LOG ====="
cat logs/worker_events.log

echo
echo "===== TREE ====="
tree -L 3
