#!/bin/bash
# discover.sh — Ping all registered BlackRoad devices and report status
# Usage: ./scripts/discover.sh

set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${CYAN}  BlackRoad Hardware Fleet — Network Discovery${NC}"
echo -e "${CYAN}  $(date '+%Y-%m-%d %H:%M:%S')${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

ONLINE=0
OFFLINE=0
TOTAL=0

check_host() {
    local name="$1"
    local ip="$2"
    local role="$3"
    TOTAL=$((TOTAL + 1))

    if ping -c 1 -W 2 "$ip" > /dev/null 2>&1; then
        printf "  ${GREEN}●${NC} %-14s %-18s %s\n" "$name" "$ip" "$role"
        ONLINE=$((ONLINE + 1))
    else
        printf "  ${RED}○${NC} %-14s %-18s %s\n" "$name" "$ip" "$role"
        OFFLINE=$((OFFLINE + 1))
    fi
}

echo -e "${CYAN}LAN Devices (192.168.4.0/24)${NC}"
echo ""
check_host "meridian"    "192.168.4.1"   "Router"
check_host "ember"       "192.168.4.22"  "IoT"
check_host "pandora"     "192.168.4.26"  "TV"
check_host "cordelia"    "192.168.4.27"  "Orchestration (Pi 5)"
check_host "alexandria"  "192.168.4.28"  "Command Center (Mac M1)"
check_host "calliope"    "192.168.4.33"  "Streaming (Roku Stick)"
check_host "octavia"     "192.168.4.38"  "Primary Compute (Pi 5+Pironman+H8)"
check_host "wraith"      "192.168.4.44"  "Unknown (silent)"
check_host "vesper"      "192.168.4.45"  "Unknown (silent)"
check_host "alice"       "192.168.4.49"  "Gateway (Pi 400)"
check_host "lucidia"     "192.168.4.81"  "AI Inference (Pi 5+ElectroCookie)"
check_host "aria"        "192.168.4.82"  "API Services (Pi 5+Pironman+H8)"
check_host "phantom"     "192.168.4.88"  "Mobile (privacy MAC)"
check_host "cecilia"     "192.168.4.89"  "Primary AI / CECE OS (Pi 5+H8)"
check_host "cortana"     "192.168.4.90"  "Console (Xbox/Surface)"
check_host "specter"     "192.168.4.92"  "Mobile (privacy MAC)"

echo ""
echo -e "${CYAN}Cloud Nodes (DigitalOcean)${NC}"
echo ""
check_host "anastasia"   "174.138.44.45" "Edge Compute / Shellfish"
check_host "gematria"    "159.65.43.12"  "Cloud Oracle / Codex-Infinity"

echo ""
echo -e "${CYAN}Tailscale Mesh${NC}"
echo ""
check_host "cecilia-ts"  "100.72.180.98"  "cecilia via Tailscale"
check_host "octavia-ts"  "100.66.235.47"  "octavia via Tailscale"
check_host "alice-ts"    "100.77.210.18"  "alice via Tailscale"
check_host "lucidia-ts"  "100.83.149.86"  "lucidia via Tailscale"
check_host "aria-ts"     "100.109.14.17"  "aria via Tailscale"

echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "  Total: ${TOTAL}  ${GREEN}Online: ${ONLINE}${NC}  ${RED}Offline: ${OFFLINE}${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
