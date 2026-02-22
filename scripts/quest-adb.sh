#!/usr/bin/env bash
# quest-adb.sh — BlackRoad ADB management for Meta Quest (andromeda)
set -euo pipefail

ADB="/Users/alexa/Library/Application Support/SideQuest/platform-tools/adb"
QUEST_NAME="andromeda"
QUEST_IP="${QUEST_IP:-}"   # Set via env or detected
ADB_PORT=5555
GATEWAY_URL="${BLACKROAD_GATEWAY_URL:-http://192.168.4.89:8787}"

# Colors
GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'
log()   { echo -e "${GREEN}✓${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1" >&2; }
info()  { echo -e "${CYAN}ℹ${NC} $1"; }
warn()  { echo -e "${YELLOW}⚠${NC} $1"; }

adb() { "$ADB" "$@"; }

# ── Helpers ───────────────────────────────────────────────────────────────────

get_quest_ip() {
  "$ADB" shell ip addr show wlan0 2>/dev/null \
    | grep "inet " | awk '{print $2}' | cut -d/ -f1
}

assert_connected() {
  if ! "$ADB" devices | grep -q "device$"; then
    error "No Quest connected. Connect USB or run: $0 wifi-connect <IP>"
    exit 1
  fi
}

# ── Commands ──────────────────────────────────────────────────────────────────

cmd_devices() {
  info "Scanning for ADB devices..."
  "$ADB" devices -l
}

cmd_status() {
  assert_connected
  echo ""
  echo -e "${CYAN}═══ ${QUEST_NAME} (Meta Quest 2) ═══${NC}"
  echo ""
  MODEL=$("$ADB" shell getprop ro.product.model 2>/dev/null | tr -d '\r')
  OS=$("$ADB" shell getprop ro.build.version.release 2>/dev/null | tr -d '\r')
  SERIAL=$("$ADB" get-serialno 2>/dev/null | tr -d '\r')
  IP=$(get_quest_ip)
  BATTERY=$("$ADB" shell dumpsys battery 2>/dev/null | grep "level:" | awk '{print $2}' | tr -d '\r')
  MEM=$("$ADB" shell cat /proc/meminfo 2>/dev/null | grep "MemFree:" | awk '{print $2}')
  MEM_MB=$((${MEM:-0} / 1024))

  printf "  %-18s %s\n" "Model:"    "${MODEL}"
  printf "  %-18s %s\n" "OS:"       "Android ${OS} (Horizon OS)"
  printf "  %-18s %s\n" "Serial:"   "${SERIAL}"
  printf "  %-18s %s\n" "WiFi IP:"  "${IP:-unknown}"
  printf "  %-18s %s%%\n" "Battery:" "${BATTERY:-?}"
  printf "  %-18s %s MB free\n" "Memory:"   "${MEM_MB}"
  echo ""

  # Check Termux
  if "$ADB" shell pm list packages 2>/dev/null | grep -q "com.termux"; then
    log "Termux installed"
  else
    warn "Termux not installed — run: $0 install-termux"
  fi
}

cmd_wifi_enable() {
  assert_connected
  info "Enabling WiFi ADB on port ${ADB_PORT}..."
  IP=$(get_quest_ip)
  "$ADB" tcpip ${ADB_PORT}
  log "WiFi ADB enabled — connect with: $0 wifi-connect ${IP}"
  echo "  Quest IP: ${IP}"
}

cmd_wifi_connect() {
  local ip="${1:-$QUEST_IP}"
  if [[ -z "$ip" ]]; then
    error "Usage: $0 wifi-connect <quest-ip>"
    exit 1
  fi
  info "Connecting to ${ip}:${ADB_PORT}..."
  "$ADB" connect "${ip}:${ADB_PORT}"
  sleep 1
  "$ADB" devices
}

cmd_shell() {
  assert_connected
  info "Opening ADB shell on ${QUEST_NAME}..."
  "$ADB" shell
}

cmd_termux_shell() {
  assert_connected
  info "Opening Termux shell on ${QUEST_NAME}..."
  # Run a shell inside Termux's environment
  "$ADB" shell run-as com.termux /data/data/com.termux/files/usr/bin/bash
}

cmd_install_termux() {
  local APK_PATH="${1:-}"
  if [[ -z "$APK_PATH" ]]; then
    error "Usage: $0 install-termux <path/to/termux.apk>"
    info "Download from: https://f-droid.org/packages/com.termux/"
    exit 1
  fi
  assert_connected
  info "Installing Termux..."
  "$ADB" install -r "$APK_PATH"
  log "Termux installed. Launch it from the Quest headset first to initialize."
}

cmd_install_apk() {
  local APK_PATH="${1:-}"
  if [[ -z "$APK_PATH" ]]; then
    error "Usage: $0 install <path/to/app.apk>"
    exit 1
  fi
  assert_connected
  info "Installing ${APK_PATH}..."
  "$ADB" install -r "$APK_PATH"
  log "Installed."
}

cmd_push() {
  local src="${1:-}" dst="${2:-/sdcard/}"
  if [[ -z "$src" ]]; then
    error "Usage: $0 push <local-file> [remote-path]"
    exit 1
  fi
  assert_connected
  info "Pushing ${src} → ${dst}..."
  "$ADB" push "$src" "$dst"
  log "Done."
}

cmd_pull() {
  local src="${1:-}" dst="${2:-.}"
  if [[ -z "$src" ]]; then
    error "Usage: $0 pull <remote-path> [local-dest]"
    exit 1
  fi
  assert_connected
  "$ADB" pull "$src" "$dst"
  log "Pulled to ${dst}."
}

cmd_bootstrap_agents() {
  assert_connected
  info "Bootstrapping BlackRoad agents on ${QUEST_NAME}..."

  # Check Termux
  if ! "$ADB" shell pm list packages 2>/dev/null | grep -q "com.termux"; then
    error "Termux not installed. Run: $0 install-termux <path/to/termux.apk> first"
    exit 1
  fi

  # Create bootstrap script
  BOOTSTRAP=$(cat << 'BASH'
#!/data/data/com.termux/files/usr/bin/bash
set -e
echo "=== BlackRoad Agent Bootstrap ==="
pkg update -y && pkg upgrade -y
pkg install -y python git curl wget openssh
pip install requests httpx websocket-client pyyaml 2>&1 | tail -5
echo "=== Cloning blackroad-agents ==="
cd ~ && git clone https://github.com/BlackRoad-OS-Inc/blackroad-agents.git || (cd blackroad-agents && git pull)
echo "Bootstrap complete."
BASH
)

  echo "$BOOTSTRAP" > /tmp/br-bootstrap.sh
  "$ADB" push /tmp/br-bootstrap.sh /sdcard/br-bootstrap.sh
  rm /tmp/br-bootstrap.sh

  log "Bootstrap script pushed to /sdcard/br-bootstrap.sh"
  info "Now in the Quest:"
  info "  1. Open Termux"
  info "  2. Run: cp /sdcard/br-bootstrap.sh ~ && bash ~/br-bootstrap.sh"
  warn "Or use: $0 termux-shell  then run the script"
}

cmd_logcat() {
  assert_connected
  local tag="${1:-BlackRoad}"
  info "Streaming logs (tag: ${tag}) — Ctrl+C to stop..."
  "$ADB" logcat -s "${tag}:*" "*:E"
}

cmd_ping_gateway() {
  assert_connected
  info "Testing Quest → BlackRoad gateway (${GATEWAY_URL})..."
  RESULT=$("$ADB" shell "curl -sf ${GATEWAY_URL}/health" 2>/dev/null || echo "FAIL")
  if [[ "$RESULT" != "FAIL" && -n "$RESULT" ]]; then
    log "Gateway reachable from Quest: ${RESULT}"
  else
    warn "Gateway not reachable. Check Quest is on same WiFi as Pi cluster."
    info "Quest IP: $(get_quest_ip)"
    info "Expected gateway: ${GATEWAY_URL}"
  fi
}

cmd_info() {
  echo ""
  info "quest-adb.sh — BlackRoad Quest management"
  echo ""
  echo "  ADB path:  $ADB"
  echo "  ADB ver:   $("$ADB" version | head -1)"
  echo "  Gateway:   ${GATEWAY_URL}"
  echo ""
}

show_help() {
  cat << HELP
quest-adb — BlackRoad ADB manager for ${QUEST_NAME} (Meta Quest 2)

Usage: $(basename "$0") <command> [args]

Commands:
  devices              List connected ADB devices
  status               Show Quest hardware status
  wifi-enable          Enable WiFi ADB (run via USB first)
  wifi-connect <ip>    Connect wirelessly via ADB
  shell                Open ADB shell
  termux-shell         Open Termux bash shell
  install-termux <apk> Install Termux from APK file
  install <apk>        Install any APK
  push <file> [dest]   Push file to Quest
  pull <src> [dest]    Pull file from Quest
  bootstrap-agents     Bootstrap BlackRoad agents in Termux
  ping-gateway         Test Quest → BlackRoad gateway connectivity
  logcat [tag]         Stream device logs
  info                 Show tool info

Environment:
  QUEST_IP             Pre-set Quest IP for WiFi ADB
  BLACKROAD_GATEWAY_URL Gateway URL (default: http://192.168.4.89:8787)

Examples:
  $(basename "$0") devices
  $(basename "$0") wifi-enable            # Enable WiFi ADB (USB connected)
  $(basename "$0") wifi-connect 192.168.4.55
  $(basename "$0") status
  $(basename "$0") bootstrap-agents
  $(basename "$0") push ./my-agent.py /sdcard/
HELP
}

# ── Router ────────────────────────────────────────────────────────────────────

case "${1:-help}" in
  devices)          cmd_devices ;;
  status)           cmd_status ;;
  wifi-enable)      cmd_wifi_enable ;;
  wifi-connect)     cmd_wifi_connect "${2:-}" ;;
  shell)            cmd_shell ;;
  termux-shell)     cmd_termux_shell ;;
  install-termux)   cmd_install_termux "${2:-}" ;;
  install)          cmd_install_apk "${2:-}" ;;
  push)             cmd_push "${2:-}" "${3:-/sdcard/}" ;;
  pull)             cmd_pull "${2:-}" "${3:-.}" ;;
  bootstrap-agents) cmd_bootstrap_agents ;;
  ping-gateway)     cmd_ping_gateway ;;
  logcat)           cmd_logcat "${2:-BlackRoad}" ;;
  info)             cmd_info ;;
  help|--help|-h)   show_help ;;
  *)                error "Unknown command: $1"; show_help; exit 1 ;;
esac
