#!/bin/bash

ENDPOINTS=("/" "/api/data" "/health")

for i in {1..100}; do
    ENDPOINT=${ENDPOINTS[$RANDOM % ${#ENDPOINTS[@]}]}
    curl -s "http://localhost:8000$ENDPOINT" > /dev/null
    sleep 0.$((RANDOM % 5 + 1))
done

echo "Load generation complete"
