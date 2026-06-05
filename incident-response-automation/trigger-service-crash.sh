#!/bin/bash
set -e

echo "Triggering service crash incident..."

sudo cp /etc/nginx/sites-available/incident-app /etc/nginx/sites-available/incident-app.backup

sudo sed -i 's/listen 8080;/listen BROKEN_PORT;/' /etc/nginx/sites-available/incident-app

sudo systemctl stop nginx || true
sudo nginx -t || true

echo "Service crash incident triggered"
