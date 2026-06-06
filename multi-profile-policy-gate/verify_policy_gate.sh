#!/bin/bash
set -e

echo "===== HEALTH ====="
curl -s http://localhost:8080/health | jq

echo
echo "===== PROFILES ====="
curl -s http://localhost:8080/profiles | jq

echo
echo "===== HEALTHCARE NON-COMPLIANT ====="
curl -s -X POST http://localhost:8080/switch-profile \
  -H "Content-Type: application/json" \
  -d '{"profile": "healthcare"}' | jq

curl -s -X POST http://localhost:8080/enforce \
  -H "Content-Type: application/json" \
  -d '{"data_type":"PHI","encrypted":false,"access_logged":true,"retention_days":1200}' | jq

echo
echo "===== HEALTHCARE COMPLIANT ====="
curl -s -X POST http://localhost:8080/enforce \
  -H "Content-Type: application/json" \
  -d '{"data_type":"PHI","encrypted":true,"access_logged":true,"retention_days":1200}' | jq

echo
echo "===== FINANCE COMPLIANT ====="
curl -s -X POST http://localhost:8080/switch-profile \
  -H "Content-Type: application/json" \
  -d '{"profile": "finance"}' | jq

curl -s -X POST http://localhost:8080/enforce \
  -H "Content-Type: application/json" \
  -d '{"data_type":"cardholder_data","encrypted":true,"network_segmented":true,"password_length":14}' | jq

echo
echo "===== RETAIL NON-COMPLIANT ====="
curl -s -X POST http://localhost:8080/switch-profile \
  -H "Content-Type: application/json" \
  -d '{"profile": "retail"}' | jq

curl -s -X POST http://localhost:8080/enforce \
  -H "Content-Type: application/json" \
  -d '{"data_type":"customer_pii","encrypted":false,"request_count":1500}' | jq
