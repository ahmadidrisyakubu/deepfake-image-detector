#!/bin/sh

# Use the PORT environment variable provided by Railway, or default to 5000
PORT_NUMBER=${PORT:-5000}

echo "Starting Gunicorn on port $PORT_NUMBER..."

# Execute Gunicorn with the expanded port number
exec gunicorn app:app \
    --bind 0.0.0.0:$PORT_NUMBER \
    --workers 1 \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 50
