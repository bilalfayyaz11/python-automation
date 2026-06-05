#!/bin/bash
set -e

DRILL_TYPE=$1
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
LOG_FILE="drill-${DRILL_TYPE}-${TIMESTAMP}.log"

log_action() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

capture_state() {
  log_action "=== System State Capture ==="
  {
    echo
    echo "Date:"
    date

    echo
    echo "Disk:"
    df -h

    echo
    echo "Memory:"
    free -h

    echo
    echo "CPU:"
    top -bn1 | head -15

    echo
    echo "Ports:"
    sudo ss -tlnp | grep -E ':8080|:80|:5432' || true

    echo
    echo "Nginx:"
    systemctl status nginx --no-pager | head -12 || true
  } | tee -a "$LOG_FILE"
}

execute_drill() {
  log_action "Starting $DRILL_TYPE drill"
  capture_state

  case "$DRILL_TYPE" in
    disk)
      ./trigger-disk-full.sh | tee -a "$LOG_FILE"
      log_action "Investigating disk usage"
      df -h | tee -a "$LOG_FILE"
      sudo du -sh /tmp/* 2>/dev/null | sort -hr | head -10 | tee -a "$LOG_FILE"
      log_action "Resolving disk incident"
      sudo rm -rf /tmp/disk-fill-test
      df -h | tee -a "$LOG_FILE"
      ;;
    service)
      ./trigger-service-crash.sh | tee -a "$LOG_FILE"
      log_action "Investigating service failure"
      sudo nginx -t 2>&1 | tee -a "$LOG_FILE" || true
      journalctl -u nginx -n 30 --no-pager | tee -a "$LOG_FILE" || true
      log_action "Restoring nginx configuration"
      sudo cp /etc/nginx/sites-available/incident-app.backup /etc/nginx/sites-available/incident-app
      sudo nginx -t | tee -a "$LOG_FILE"
      sudo systemctl restart nginx
      curl -I http://localhost:8080 | tee -a "$LOG_FILE"
      ;;
    cpu)
      ./trigger-cpu-spike.sh | tee -a "$LOG_FILE"
      log_action "Investigating CPU spike"
      ps aux --sort=-%cpu | head -10 | tee -a "$LOG_FILE"
      log_action "Resolving CPU spike"
      xargs -r kill < /tmp/cpu-spike-pids.txt || true
      rm -f /tmp/cpu-spike-pids.txt
      top -bn1 | head -10 | tee -a "$LOG_FILE"
      ;;
  esac

  capture_state
  log_action "$DRILL_TYPE drill completed"
}

case "$DRILL_TYPE" in
  disk|service|cpu)
    execute_drill
    ;;
  *)
    echo "Usage: $0 {disk|service|cpu}"
    exit 1
    ;;
esac

log_action "Review log: $LOG_FILE"
