# XR Headsets

> Standalone XR devices managed in the BlackRoad fleet via ADB.

---

## Fleet Devices

| Name | Model | Status | IP | Roles |
|------|-------|--------|-----|-------|
| andromeda | Meta Quest 2 | active | TBD (WiFi ADB) | xr_interface, spatial_agent |

---

## andromeda — Meta Quest 2

### Specifications

| Property | Value |
|----------|-------|
| **SoC** | Qualcomm Snapdragon XR2 |
| **CPU** | Octa-core Kryo 585 @ 2.84GHz |
| **GPU** | Adreno 650 |
| **RAM** | 6 GB LPDDR5 |
| **Storage** | 128GB / 256GB (check `adb shell df /sdcard`) |
| **OS** | Horizon OS (Android 10 base) |
| **Display** | Dual LCD 1832×1920 per eye @ 72/90Hz |
| **Battery** | ~2–3h active use |
| **ADB** | USB (direct) + WiFi (wireless ADB) |
| **Connectivity** | WiFi 6 (802.11ax), Bluetooth 5.1 |
| **USB** | USB-C 3.0 (data + charging) |

---

## Initial Setup

### 1 — Enable Developer Mode

1. Open **Meta Quest app** on your phone
2. Go to **Menu → Devices → [your Quest 2] → Developer Mode**
3. Toggle **Developer Mode ON**
4. Reboot headset

### 2 — Connect via USB and Authorize

```bash
# Find ADB (SideQuest ships it)
ADB="/Users/alexa/Library/Application Support/SideQuest/platform-tools/adb"
alias adb="$ADB"

# Connect USB-C → Mac
adb devices
# → Accept prompt inside the headset: "Allow USB Debugging?"
# → Check "Always allow from this computer" then Allow

# Verify
adb devices
# List of devices attached
# 1WMHH123456789  device   ← should show "device" not "unauthorized"
```

### 3 — Set Up WiFi ADB (Wireless)

```bash
# While connected via USB first:
adb tcpip 5555

# Find Quest's IP in headset: Settings → WiFi → (your network) → Advanced
# Or:
adb shell ip addr show wlan0 | grep "inet "

# Disconnect USB, then:
adb connect 192.168.4.XXX:5555
adb devices
# Should show Quest as connected wirelessly
```

> 💡 Update `fleet-registry.yaml` with the Quest's actual IP once connected.

---

## Running BlackRoad Agents via Termux

Termux is an Android terminal emulator that gives you a full Linux environment on the Quest.

### Install Termux via SideQuest

1. Download **Termux** APK from [f-droid.org/packages/com.termux](https://f-droid.org/packages/com.termux/)
   - **Do NOT use the Play Store version** — it's outdated
2. Install via ADB or SideQuest:
   ```bash
   adb install termux-arm64.apk
   ```
3. Launch Termux inside the Quest (via Unknown Sources in App Library)

### Bootstrap Termux for BlackRoad

Once Termux is running (you can shell in via ADB):

```bash
# Shell into Termux from Mac
adb shell
# Then: am start -n com.termux/com.termux.HomeActivity
# Or open Termux in headset, then:
adb shell -e - "su -s /system/bin/sh com.termux"

# Inside Termux:
pkg update && pkg upgrade -y
pkg install -y python git curl wget openssh

# Install Python packages for BlackRoad agents
pip install requests httpx websocket-client pyyaml

# Clone BlackRoad agents
git clone https://github.com/BlackRoad-OS-Inc/blackroad-agents.git
cd blackroad-agents

# Run a BlackRoad agent (connects to gateway at 192.168.4.89 or cloud)
export BLACKROAD_GATEWAY_URL=http://192.168.4.89:8787  # or your Pi
python scripts/agent-runner.py
```

### Push scripts directly via ADB

```bash
# Push a script from Mac to Quest/Termux home
adb push my-agent.py /sdcard/
# Move it inside Termux to its home directory
adb shell "cp /sdcard/my-agent.py /data/data/com.termux/files/home/"
```

---

## ADB Management Reference

```bash
# ── Device info ─────────────────────────────────────────────
adb shell getprop ro.product.model          # Meta Quest 2
adb shell getprop ro.build.version.release  # Android version
adb shell getprop ro.build.version.sdk      # API level
adb shell dumpsys battery                   # Battery status
adb shell df /sdcard                        # Storage
adb shell free -h                           # Memory

# ── App management ──────────────────────────────────────────
adb install app.apk                         # Install APK
adb uninstall com.package.name             # Uninstall
adb shell pm list packages | grep termux   # Find Termux
adb shell am start -n com.termux/com.termux.HomeActivity  # Launch Termux

# ── File transfer ───────────────────────────────────────────
adb push local-file.py /sdcard/            # Mac → Quest
adb pull /sdcard/file.log ./               # Quest → Mac
adb shell ls /sdcard/                       # List files

# ── Logcat ──────────────────────────────────────────────────
adb logcat -s "BlackRoad:*"                # BlackRoad logs only
adb logcat > quest-debug.log 2>&1 &        # Capture all logs

# ── Network ─────────────────────────────────────────────────
adb shell ip addr show wlan0               # Get Quest IP
adb shell ping 192.168.4.89                # Ping Pi cluster
adb shell curl http://192.168.4.89:8787/health  # Test gateway

# ── Screenshots / screen ────────────────────────────────────
adb shell screencap -p /sdcard/screen.png
adb pull /sdcard/screen.png ./
```

---

## BlackRoad XR App (Future APK)

A custom BlackRoad XR app will be built as a Unity or native Android project and deployed via SideQuest.

Planned capabilities:
- **Spatial agent dashboard** — view fleet status in 3D space
- **Voice-to-agent** — speak commands to Octavia/Lucidia/Alice
- **Holographic memory** — visualize CECE memory graph
- **Passthrough UI** — overlay BlackRoad status on real world (Quest Pro/3 compatible)

APK will live in `blackroad-agents` repo under `apps/android/`.

---

## Roles in the Fleet

| Role | Description |
|------|-------------|
| `xr_interface` | Primary XR display node for BlackRoad visualizations |
| `spatial_agent` | Runs BlackRoad agents in Termux, connects to gateway |

---

## Network

Once WiFi ADB is set up, update `fleet-registry.yaml`:
```yaml
- name: andromeda
  ip_local: "192.168.4.XXX"   # fill in after first connection
```

The Quest should be on `192.168.4.0/24` (your LAN) for full mesh access.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `adb devices` shows `unauthorized` | Put Quest on, look for USB debugging prompt inside |
| WiFi ADB disconnects | Re-run `adb tcpip 5555` via USB, then reconnect |
| Termux can't access network | Grant network permission in Android settings |
| APK install fails `INSTALL_FAILED_VERIFICATION_FAILURE` | Enable Unknown Sources in Quest Settings > Developer |
| SideQuest shows offline | Re-enable Developer Mode in Meta app |
