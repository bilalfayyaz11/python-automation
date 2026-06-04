#!/bin/bash

echo "=== Config Generator Verification ==="
echo

if python3 -c "from generator import ConfigGenerator; print('OK')" 2>/dev/null; then
    echo "[PASS] Generator module loads"
else
    echo "[FAIL] Generator module has errors"
fi

if python3 -c "from validator import ConfigValidator; print('OK')" 2>/dev/null; then
    echo "[PASS] Validator module loads"
else
    echo "[FAIL] Validator module has errors"
fi

python3 generator.py data/prod_config.yaml >/dev/null

if [ -f configs/nginx.conf ] && [ -f configs/app_config.yaml ]; then
    echo "[PASS] Configuration files generated"
else
    echo "[FAIL] Missing configuration files"
fi

if grep -q "upstream myapp_backend" configs/nginx.conf; then
    echo "[PASS] Nginx config contains upstream block"
else
    echo "[FAIL] Nginx config missing upstream block"
fi

if python3 validator.py configs/app_config.yaml app_config_schema.json >/dev/null; then
    echo "[PASS] App config validates against schema"
else
    echo "[FAIL] App config validation failed"
fi

if python3 validator.py configs/nginx.conf nginx >/dev/null; then
    echo "[PASS] Nginx config structure validates"
else
    echo "[FAIL] Nginx config validation failed"
fi

echo
echo "=== Verification Complete ==="
