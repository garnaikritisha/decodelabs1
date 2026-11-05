#!/usr/bin/env bash
# ==============================================================================
# DecodeLabs DevOps Project 1 - Stop Web Application Server
# ==============================================================================

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PID_FILE="$PROJECT_ROOT/app/server.pid"

if [[ -f "$PID_FILE" ]]; then
    PID=$(cat "$PID_FILE")
    if kill -0 "$PID" 2>/dev/null; then
        echo "Stopping DecodeLabs DevOps server (PID: $PID)..."
        kill "$PID"
        rm -f "$PID_FILE"
        echo "✔ Server stopped."
        exit 0
    fi
fi

# Fallback: kill any python server running on port 8080
PID=$(lsof -ti :8080 || true)
if [[ -n "$PID" ]]; then
    echo "Stopping process listening on port 8080 (PID: $PID)..."
    kill "$PID"
    echo "✔ Server stopped."
else
    echo "Server is not running."
fi
