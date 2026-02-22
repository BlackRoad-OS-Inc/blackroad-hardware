#!/data/data/com.termux/files/usr/bin/bash
# quest-bootstrap.sh — Run inside Termux on andromeda to set up BlackRoad agents
#
# Push to Quest:  adb push scripts/quest-bootstrap.sh /sdcard/
# Run in Termux:  cp /sdcard/quest-bootstrap.sh ~ && bash ~/quest-bootstrap.sh
set -e

GATEWAY="${BLACKROAD_GATEWAY_URL:-http://192.168.4.89:8787}"
AGENTS_REPO="https://github.com/BlackRoad-OS-Inc/blackroad-agents.git"

echo "╔══════════════════════════════════════════╗"
echo "║  BlackRoad Agent Bootstrap — andromeda   ║"
echo "║  Meta Quest 2 / Termux                   ║"
echo "╚══════════════════════════════════════════╝"
echo ""

echo "[1/4] Updating packages..."
pkg update -y 2>&1 | tail -2
pkg upgrade -y 2>&1 | tail -2

echo "[2/4] Installing dependencies..."
pkg install -y python git curl wget openssh 2>&1 | tail -3

echo "[3/4] Installing Python packages..."
pip install --quiet requests httpx websocket-client pyyaml 2>&1 | tail -2

echo "[4/4] Cloning blackroad-agents..."
cd ~
if [ -d "blackroad-agents" ]; then
  echo "  Repo exists — pulling latest..."
  cd blackroad-agents && git pull --ff-only
else
  git clone "$AGENTS_REPO"
fi

echo ""
echo "=== Testing gateway connectivity ==="
if curl -sf --max-time 5 "$GATEWAY/health" > /dev/null 2>&1; then
  echo "  ✓ Gateway reachable at $GATEWAY"
else
  echo "  ✗ Gateway not reachable at $GATEWAY"
  echo "    Make sure you're on the 192.168.4.0/24 network"
fi

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  Bootstrap complete!                     ║"
echo "║                                          ║"
echo "║  Start agent:                            ║"
echo "║    cd ~/blackroad-agents                 ║"
echo "║    python scripts/agent-runner.py        ║"
echo "╚══════════════════════════════════════════╝"
