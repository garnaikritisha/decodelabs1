#!/usr/bin/env bash
# ==============================================================================
# DecodeLabs DevOps Project 1 - Real-Time Server Log Simulator
# Demonstrates: tail -f live monitoring in DevOps environments
# ==============================================================================

LOG_FILE="${1:-$(pwd)/app/logs/server.log}"
mkdir -p "$(dirname "$LOG_FILE")"

echo -e "\033[34m\033[1mStarting Real-Time Log Simulator...\033[0m"
echo -e "Target Log File: \033[36m$LOG_FILE\033[0m"
echo -e "\033[33mTo view logs in real time, open a second terminal and run:\033[0m"
echo -e "   \033[32mtail -f \"$LOG_FILE\"\033[0m"
echo -e "Press [Ctrl+C] to stop.\n"

ENDPOINTS=("/api/v1/health" "/api/v1/login" "/api/v1/users" "/api/v1/payments" "/dashboard" "/metrics")
STATUS_CODES=("200 OK" "200 OK" "201 Created" "404 Not Found" "500 Internal Error" "304 Not Modified")
LEVELS=("INFO" "INFO" "INFO" "WARN" "ERROR" "DEBUG")

COUNTER=1
while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    IDX=$(( RANDOM % ${#ENDPOINTS[@]} ))
    ENDPOINT="${ENDPOINTS[$IDX]}"
    STATUS="${STATUS_CODES[$IDX]}"
    LEVEL="${LEVELS[$IDX]}"
    LATENCY=$(( (RANDOM % 150) + 10 ))ms

    LOG_ENTRY="[$TIMESTAMP] [$LEVEL] [req-${COUNTER}] IP=192.168.1.$(( (RANDOM % 50) + 2 )) GET $ENDPOINT -> $STATUS in $LATENCY"
    echo "$LOG_ENTRY" >> "$LOG_FILE"
    echo "[LOG EMITTED] $LOG_ENTRY"

    COUNTER=$((COUNTER + 1))
    sleep 2
done
