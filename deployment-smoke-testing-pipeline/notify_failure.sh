#!/bin/bash

REPORT_FILE="$1"
NOTIFICATION_LOG="reports/notifications.log"

if [ -f "$REPORT_FILE" ]; then
    echo "$(date): Deployment Notification" >> "$NOTIFICATION_LOG"
    cat "$REPORT_FILE" >> "$NOTIFICATION_LOG"
    echo "---" >> "$NOTIFICATION_LOG"
fi
