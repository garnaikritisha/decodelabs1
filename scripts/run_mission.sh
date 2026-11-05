#!/usr/bin/env bash
# ==============================================================================
# DecodeLabs Industrial Training Kit – DevOps Project 1: Linux & Command Line Basics
# Mission Execution & Verification Script (Batch 2026)
# ==============================================================================

set -euo pipefail

# ANSI Color Codes for Professional Terminal Presentation
C_RESET='\033[0m'
C_BOLD='\033[1m'
C_GREEN='\033[32m'
C_BLUE='\033[34m'
C_CYAN='\033[36m'
C_YELLOW='\033[33m'
C_MAGENTA='\033[35m'
C_RED='\033[31m'

print_header() {
    echo -e "${C_BLUE}${C_BOLD}"
    echo "=============================================================================="
    echo "  DECODELABS INDUSTRIAL TRAINING KIT - DEVOPS BATCH 2026"
    echo "  Project 1: Linux & Command Line Basics - Mission Runner"
    echo "=============================================================================="
    echo -e "${C_RESET}"
}

print_step() {
    local step_num="$1"
    local title="$2"
    echo -e "\n${C_MAGENTA}${C_BOLD}[STEP $step_num] $title${C_RESET}"
    echo -e "${C_CYAN}------------------------------------------------------------------------------${C_RESET}"
}

print_command() {
    echo -e "${C_YELLOW}$ ${C_BOLD}$*${C_RESET}"
}

print_success() {
    echo -e "${C_GREEN}✔ PASS: $*${C_RESET}"
}

# Determine base directory
# If executed with argument, use that; otherwise use local ./app for macOS safe execution
TARGET_BASE="${1:-$(pwd)/app}"

print_header

echo -e "${C_BOLD}Execution Environment Information:${C_RESET}"
echo -e "  • Operating System : $(uname -s) ($(uname -m))"
echo -e "  • Kernel Version   : $(uname -r)"
echo -e "  • Current User     : $(whoami)"
echo -e "  • User ID & Groups : $(id)"
echo -e "  • Target App Path  : ${TARGET_BASE}"
echo -e ""

if [[ "${TARGET_BASE}" == "/app" && "$EUID" -ne 0 ]]; then
    echo -e "${C_YELLOW}⚠ NOTICE: Target path is root '/app'. This typically requires administrator (sudo) privileges.${C_RESET}"
    echo -e "${C_YELLOW}If permission is denied, consider using a local path: ./scripts/run_mission.sh $(pwd)/app${C_RESET}\n"
fi

# ==============================================================================
# MISSION EXECUTION
# ==============================================================================

print_step "1" "Create directory structure using 'mkdir -p'"
print_command "mkdir -p ${TARGET_BASE}/logs"
mkdir -p "${TARGET_BASE}/logs"
if [[ -d "${TARGET_BASE}/logs" ]]; then
    print_success "Directory '${TARGET_BASE}/logs' created successfully."
fi

print_step "2" "Create configuration file using 'touch'"
print_command "touch ${TARGET_BASE}/config.conf"
touch "${TARGET_BASE}/config.conf"

# Populate with a realistic production configuration template
cat << 'EOF' > "${TARGET_BASE}/config.conf"
# ----------------------------------------------------
# DecodeLabs DevOps Project 1 - Application Configuration
# Environment: Production-Ready Baseline
# ----------------------------------------------------
PORT=8080
HOST=0.0.0.0
APP_NAME=DecodeLabs-DevOps-App
ENVIRONMENT=production
LOG_LEVEL=info
LOG_DIR=/app/logs
MAX_CONNECTIONS=1000
EOF
if [[ -f "${TARGET_BASE}/config.conf" ]]; then
    print_success "File '${TARGET_BASE}/config.conf' created and configured."
fi

print_step "3" "Write 'Started' into server.log using 'echo'"
print_command "echo 'Started' > ${TARGET_BASE}/logs/server.log"
echo "Started" > "${TARGET_BASE}/logs/server.log"
# Append a timestamp for realistic auditability
echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] Application service initialized successfully." >> "${TARGET_BASE}/logs/server.log"
if grep -q "Started" "${TARGET_BASE}/logs/server.log"; then
    print_success "Verified 'Started' content written to '${TARGET_BASE}/logs/server.log'."
    echo -e "${C_CYAN}Current content of server.log:${C_RESET}"
    cat "${TARGET_BASE}/logs/server.log"
fi

print_step "4" "Verify working directory & application structure using 'pwd' and 'ls -R'"
print_command "pwd"
pwd
echo ""
print_command "ls -R ${TARGET_BASE}"
ls -R "${TARGET_BASE}"
print_success "Application tree successfully verified."

print_step "5" "Back up the log using 'mv'"
print_command "mv ${TARGET_BASE}/logs/server.log ${TARGET_BASE}/logs/server.bak"
mv "${TARGET_BASE}/logs/server.log" "${TARGET_BASE}/logs/server.bak"
if [[ -f "${TARGET_BASE}/logs/server.bak" && ! -f "${TARGET_BASE}/logs/server.log" ]]; then
    print_success "server.log successfully renamed/backed up to server.bak."
    echo -e "${C_CYAN}Content of backup file (${TARGET_BASE}/logs/server.bak):${C_RESET}"
    cat "${TARGET_BASE}/logs/server.bak"
fi

print_step "6" "Audit configuration file using 'ls -l'"
print_command "ls -l ${TARGET_BASE}/config.conf"
ls -l "${TARGET_BASE}/config.conf"
print_success "Configuration file audited."

# ==============================================================================
# EXTENDED DEVOPS PERMISSIONS & AUDITING DEMO
# ==============================================================================

print_step "7" "Demonstrate File Permissions & chmod 754"
print_command "chmod 754 ${TARGET_BASE}/config.conf"
chmod 754 "${TARGET_BASE}/config.conf"
print_command "ls -l ${TARGET_BASE}/config.conf"
ls -l "${TARGET_BASE}/config.conf"
echo -e "${C_CYAN}Permission Breakdown for 754 (-rwxr-xr--):"
echo -e "  • Owner (7 = 4+2+1) : Read (4) + Write (2) + Execute (1) -> rwx"
echo -e "  • Group (5 = 4+0+1) : Read (4) + Execute (1)            -> r-x"
echo -e "  • Other (4 = 4+0+0) : Read (4) only                     -> r--${C_RESET}"
print_success "Permission 754 applied and verified."

echo -e "\n${C_GREEN}${C_BOLD}==============================================================================${C_RESET}"
echo -e "${C_GREEN}${C_BOLD}  ALL MISSION STEPS COMPLETED SUCCESSFULLY!${C_RESET}"
echo -e "${C_GREEN}${C_BOLD}==============================================================================${C_RESET}\n"
