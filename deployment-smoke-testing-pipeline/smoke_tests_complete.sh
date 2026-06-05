#!/bin/bash

APP_URL="http://localhost:3000"
REPORT_FILE="reports/smoke_test_report_$(date +%Y%m%d_%H%M%S).txt"
FAILED_TESTS=0
PASSED_TESTS=0

mkdir -p reports

echo "=== Smoke Test Report ===" > "$REPORT_FILE"
echo "Timestamp: $(date)" >> "$REPORT_FILE"
echo "Target: $APP_URL" >> "$REPORT_FILE"
echo "" >> "$REPORT_FILE"

log_test() {
    echo "$1" | tee -a "$REPORT_FILE"
}

test_health_endpoint() {
    log_test "Test 1: Health Endpoint Check"

    response=$(curl -s -w "\n%{http_code}" "$APP_URL/health")
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | head -n-1)

    if [ "$http_code" = "200" ] && echo "$body" | grep -q "ok"; then
        log_test "  [PASS] Health endpoint returned 200 with ok status"
        ((PASSED_TESTS++))
    else
        log_test "  [FAIL] Health endpoint check failed"
        ((FAILED_TESTS++))
    fi
}

test_api_endpoint() {
    log_test "Test 2: API Data Endpoint Check"

    response=$(curl -s "$APP_URL/api/data")

    if echo "$response" | grep -q "version"; then
        log_test "  [PASS] API endpoint returned valid data"
        ((PASSED_TESTS++))
    else
        log_test "  [FAIL] API endpoint returned invalid response"
        ((FAILED_TESTS++))
    fi
}

test_response_time() {
    log_test "Test 3: Response Time Check"

    response_time=$(curl -o /dev/null -s -w "%{time_total}" "$APP_URL/health")

    if (( $(echo "$response_time < 2.0" | bc -l) )); then
        log_test "  [PASS] Response time ${response_time}s"
        ((PASSED_TESTS++))
    else
        log_test "  [FAIL] Response time exceeded threshold"
        ((FAILED_TESTS++))
    fi
}

test_app_status() {
    log_test "Test 4: Application Status Check"

    response=$(curl -s "$APP_URL/api/status")

    if echo "$response" | grep -q "healthy"; then
        log_test "  [PASS] Application status healthy"
        ((PASSED_TESTS++))
    else
        log_test "  [FAIL] Application unhealthy"
        ((FAILED_TESTS++))
    fi
}

echo "Starting smoke tests..."

test_health_endpoint
test_api_endpoint
test_response_time
test_app_status

log_test ""
log_test "=== Test Summary ==="
log_test "Passed: $PASSED_TESTS"
log_test "Failed: $FAILED_TESTS"

if [ $FAILED_TESTS -gt 0 ]; then
    exit 1
else
    exit 0
fi
