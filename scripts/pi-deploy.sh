#!/bin/zsh
# BlackRoad Pi Fleet Deploy — push code to all registered Pis
#
# Usage:
#   ./pi-deploy.sh [service] [--pi <name>]
#   ./pi-deploy.sh all           # deploy to all Pis
#   ./pi-deploy.sh agents        # deploy agent runtime
#   ./pi-deploy.sh --pi lucidia  # deploy to specific Pi

set -euo pipefail

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; CYAN='\033[0;36m'; NC='\033[0m'

# Pi inventory (from fleet-registry.yaml)
declare -A PI_HOSTS=(
  [blackroad-pi]="192.168.4.64"
  [lucidia]="192.168.4.38"
  [alice]="192.168.4.99"
)
PI_USER="pi"
DEPLOY_DIR="/home/pi/blackroad"

log()   { echo -e "${GREEN}✓${NC} $1"; }
warn()  { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✗${NC} $1" >&2; }

deploy_to_pi() {
  local name="$1"
  local ip="${PI_HOSTS[$name]:-}"
  if [[ -z "$ip" ]]; then
    error "Unknown Pi: $name"
    return 1
  fi

  echo -e "${CYAN}Deploying to $name ($ip)...${NC}"

  # Check connectivity
  if ! ping -c 1 -W 2 "$ip" &>/dev/null; then
    warn "$name ($ip) unreachable — skipping"
    return 0
  fi

  # Sync files
  rsync -avz --exclude='.git' --exclude='node_modules' --exclude='*.db' \
    "$DEPLOY_DIR/" "$PI_USER@$ip:$DEPLOY_DIR/" 2>/dev/null

  # Restart services if needed
  ssh "$PI_USER@$ip" "
    cd $DEPLOY_DIR
    [ -f package.json ] && npm install --production --silent 2>/dev/null || true
    sudo systemctl restart blackroad-agent 2>/dev/null || true
  " 2>/dev/null

  log "$name deployed"
}

case "${1:-all}" in
  all)
    for name in ${(k)PI_HOSTS}; do
      deploy_to_pi "$name"
    done
    ;;
  --pi)
    deploy_to_pi "${2:?Pi name required}"
    ;;
  *)
    for name in ${(k)PI_HOSTS}; do
      deploy_to_pi "$name"
    done
    ;;
esac
