#!/bin/zsh
# BlackRoad Pi Health Monitor — runs on each Pi, reports to mesh
# Interval: 60s. Sends to blackroad-mesh if available.

set -euo pipefail
GATEWAY="${BLACKROAD_GATEWAY_URL:-http://127.0.0.1:8787}"
HOSTNAME=$(hostname)
INTERVAL="${HEALTH_INTERVAL:-60}"

collect_metrics() {
  local cpu mem temp disk ip
  cpu=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1 2>/dev/null || echo "0")
  mem=$(free -m | awk 'NR==2{printf "%.1f", $3*100/$2}' 2>/dev/null || echo "0")
  temp=$(vcgencmd measure_temp 2>/dev/null | grep -o '[0-9.]*' || cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null | awk '{printf "%.1f", $1/1000}' || echo "0")
  disk=$(df / | awk 'NR==2{print $5}' | tr -d '%' || echo "0")
  ip=$(hostname -I | awk '{print $1}')

  echo "{\"hostname\":\"$HOSTNAME\",\"ip\":\"$ip\",\"cpu\":$cpu,\"mem\":$mem,\"temp\":$temp,\"disk\":$disk,\"ts\":$(date +%s)}"
}

report() {
  local payload
  payload=$(collect_metrics)
  curl -sf -X POST "$GATEWAY/v1/metrics/pi" \
    -H "Content-Type: application/json" \
    -d "$payload" 2>/dev/null || true
  echo "[$HOSTNAME] $(date '+%H:%M:%S') — $(echo "$payload" | python3 -c 'import sys,json; d=json.load(sys.stdin); print(f"CPU:{d[\"cpu\"]}% MEM:{d[\"mem\"]}% TEMP:{d[\"temp\"]}°C DISK:{d[\"disk\"]}%")')"
}

echo "BlackRoad Pi Health Monitor starting on $HOSTNAME (interval: ${INTERVAL}s)"
while true; do
  report
  sleep "$INTERVAL"
done
