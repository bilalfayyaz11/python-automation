#!/bin/bash

echo "Starting deployment..."

pkill -f "node app/server.js" 2>/dev/null || true
sleep 2

cd ~/smoke-test-pipeline

nohup node app/server.js > app.log 2>&1 &

sleep 3

echo "Deployment completed"
echo "Application PID: $(pgrep -f 'node app/server.js')"
