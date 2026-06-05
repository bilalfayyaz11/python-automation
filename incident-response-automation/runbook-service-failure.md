# Runbook: Service Failure

## Detection

```bash
systemctl status nginx --no-pager
sudo ss -tlnp | grep :8080 || echo "Port 8080 not listening"
curl -I http://localhost:8080
