#!/usr/bin/env bash
# ==============================================================================
# DecodeLabs DevOps Project 1 - Start Web Application Server
# ==============================================================================

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PID_FILE="$PROJECT_ROOT/app/server.pid"

if [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null; then
    echo "Server is already running (PID: $(cat "$PID_FILE"))."
    echo "Dashboard: http://localhost:8080"
    exit 0
fi

echo "Starting DecodeLabs DevOps Web Application Server..."
python3 "$PROJECT_ROOT/app/server.py" &
SERVER_PID=$!

sleep 1
if kill -0 "$SERVER_PID" 2>/dev/null; then
    echo "✔ Server started successfully (PID: $SERVER_PID)"
    echo "Open your browser at: http://localhost:8080"
else
    echo "❌ Server failed to start."
    exit 1
fi
