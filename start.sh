#!/bin/sh

# Railway standard port is 8080. Hardcoding it to bypass environment variable expansion issues.
PORT_NUMBER=8080

echo "Starting Gunicorn on port $PORT_NUMBER..."

# Execute Gunicorn with the hardcoded port number
exec gunicorn app:app \
    --bind 0.0.0.0:$PORT_NUMBER \
    --workers 1 \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 50
