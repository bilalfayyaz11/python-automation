#!/bin/bash

set -e

PIPELINE_LOG="reports/pipeline_$(date +%Y%m%d_%H%M%S).log"

mkdir -p reports

log_pipeline() {
    echo "[$(date +%H:%M:%S)] $1" | tee -a "$PIPELINE_LOG"
}

pre_deployment_checks() {

    if lsof -i:3000 >/dev/null 2>&1; then
        pkill -f "node app/server.js" || true
        sleep 2
    fi

    [ -f app/server.js ] || exit 1
}

deploy_application() {

    ./deploy.sh >> "$PIPELINE_LOG" 2>&1

    sleep 5

    pgrep -f "node app/server.js" >/dev/null
}

run_smoke_tests() {

    ./tests/smoke_tests_complete.sh
}

handle_results() {

    latest_report=$(ls -t reports/smoke_test_report_*.txt | head -n1)

    ./tests/notify_failure.sh "$latest_report"
}

log_pipeline "Starting deployment pipeline"

pre_deployment_checks

deploy_application

run_smoke_tests

test_exit_code=$?

handle_results

exit $test_exit_code
