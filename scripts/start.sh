#!/bin/bash

# FastAPI multi-environment startup script
# Usage: ./scripts/start.sh (defaults to dev)
#        ENVFLAG=beta ./scripts/start.sh
#        ENVFLAG=prod ./scripts/start.sh

set -e

ENVFLAG=${ENVFLAG:-dev}

case "$ENVFLAG" in
    "beta")
        SERVER="gunicorn"
        HOST="0.0.0.0"
        PORT="8000"
        EXTRA_ARGS="--workers 2 --worker-class uvicorn.workers.UvicornWorker"
        LOG_LEVEL="info"
        ;;
    "prod")
        SERVER="gunicorn"
        HOST="0.0.0.0"
        PORT="8000"
        EXTRA_ARGS="--workers 4 --worker-class uvicorn.workers.UvicornWorker"
        LOG_LEVEL="info"
        ;;
    *)
        # Default to dev environment
        SERVER="uvicorn"
        HOST="127.0.0.1"
        PORT="8000"
        EXTRA_ARGS="--reload"
        LOG_LEVEL="debug"
        ENVFLAG="dev"
        ;;
esac

ENV_FILE=".env.$ENVFLAG"

if [ ! -f "$ENV_FILE" ]; then
    echo "Environment file not found: $ENV_FILE"
    echo "Please copy .env.example to $ENV_FILE and configure the values"
    exit 1
fi

echo "Starting $ENVFLAG environment..."
echo "Environment file: $ENV_FILE"
echo "Server: $SERVER"
echo "Address: http://$HOST:$PORT"
echo ""

if [ "$SERVER" = "uvicorn" ]; then
    exec uv run uvicorn src.main:app --host $HOST --port $PORT $EXTRA_ARGS --log-level $LOG_LEVEL
else
    exec uv run gunicorn src.main:app --bind $HOST:$PORT $EXTRA_ARGS --log-level $LOG_LEVEL
fi
