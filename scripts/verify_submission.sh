#!/usr/bin/env bash
# ==============================================================================
# DecodeLabs Industrial Training Kit – DevOps Project 1: Linux & Command Line Basics
# Submission Audit & Readiness Verification Script (Batch 2026)
# ==============================================================================

set -uo pipefail

C_RESET='\033[0m'
C_BOLD='\033[1m'
C_GREEN='\033[32m'
C_BLUE='\033[34m'
C_CYAN='\033[36m'
C_YELLOW='\033[33m'
C_RED='\033[31m'

PASSED_CHECKS=0
TOTAL_CHECKS=0

check_item() {
    local desc="$1"
    local condition="$2"
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if eval "$condition"; then
        echo -e "  [${C_GREEN}PASS${C_RESET}] $desc"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
    else
        echo -e "  [${C_RED}FAIL${C_RESET}] $desc"
    fi
}

echo -e "\n${C_BLUE}${C_BOLD}==============================================================================${C_RESET}"
echo -e "${C_BLUE}${C_BOLD}  DECODELABS DEVOPS PROJECT 1 - SUBMISSION AUDIT REPORT${C_RESET}"
echo -e "${C_BLUE}${C_BOLD}==============================================================================${C_RESET}\n"

echo -e "${C_BOLD}1. Mandatory Mission Checklist Verification:${C_RESET}"
check_item "Directory 'app/logs' exists" "[[ -d 'app/logs' ]]"
check_item "Configuration file 'app/config.conf' exists" "[[ -f 'app/config.conf' ]]"
check_item "Backup log file 'app/logs/server.bak' exists" "[[ -f 'app/logs/server.bak' ]]"
check_item "server.bak contains 'Started'" "grep -q 'Started' app/logs/server.bak"
check_item "config.conf has valid file permissions (754 or 644)" "[[ \$(uname) == 'Darwin' ]] && ls -l app/config.conf | grep -E -q 'rwxr-xr--|rw-r--r--' || stat -c '%a' app/config.conf | grep -E -q '754|644'"

echo -e "\n${C_BOLD}2. Project Deliverables Verification:${C_RESET}"
check_item "Professional README.md exists and is populated (>1KB)" "[[ -f 'README.md' && \$(wc -c < 'README.md') -gt 1000 ]]"
check_item "Formal PROJECT_REPORT.md exists and is populated (>1KB)" "[[ -f 'PROJECT_REPORT.md' && \$(wc -c < 'PROJECT_REPORT.md') -gt 1000 ]]"
check_item "Automation script 'scripts/run_mission.sh' is executable" "[[ -x 'scripts/run_mission.sh' ]]"
check_item "Log simulator script 'scripts/simulate_logs.sh' is executable" "[[ -x 'scripts/simulate_logs.sh' ]]"

echo -e "\n${C_BOLD}3. System Context Snapshot:${C_RESET}"
echo -e "  • User            : $(whoami)"
echo -e "  • Working Dir     : $(pwd)"
echo -e "  • Date of Audit   : $(date)"
echo -e "  • OS & Kernel     : $(uname -s) $(uname -r) ($(uname -m))"

echo -e "\n${C_BOLD}Summary:${C_RESET}"
if [[ $PASSED_CHECKS -eq $TOTAL_CHECKS ]]; then
    echo -e "${C_GREEN}${C_BOLD}✔ PERFECT SCORE: $PASSED_CHECKS/$TOTAL_CHECKS checks passed. 100% submission ready!${C_RESET}\n"
else
    echo -e "${C_YELLOW}${C_BOLD}⚠ STATUS: $PASSED_CHECKS/$TOTAL_CHECKS checks passed. Please review any failed items above.${C_RESET}\n"
fi
