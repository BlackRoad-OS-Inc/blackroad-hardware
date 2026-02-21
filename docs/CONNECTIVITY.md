# Connectivity Guide

How to connect to every device in the BlackRoad fleet.

---

## SSH Access (Compute Nodes)

### Local Network (192.168.4.x)

```bash
ssh pi@192.168.4.89        # cecilia  (Pi 5 + Hailo-8, CECE OS)
ssh pi@192.168.4.38        # octavia  (Pi 5 + Pironman + Hailo-8)
ssh alice@192.168.4.49     # alice    (Pi 400) — note: user is "alice"
ssh pi@192.168.4.81        # lucidia  (Pi 5 + ElectroCookie)
ssh pi@192.168.4.82        # aria     (Pi 5 + Pironman + Hailo-8)
ssh pi@192.168.4.27        # cordelia (Pi 5, orchestration)
```

### Tailscale (Remote Access)

Use these IPs when not on the local network:

```bash
ssh pi@100.72.180.98       # cecilia
ssh pi@100.66.235.47       # octavia
ssh alice@100.77.210.18    # alice
ssh pi@100.83.149.86       # lucidia
ssh pi@100.109.14.17       # aria
```

### Cloud Nodes

```bash
ssh root@174.138.44.45     # anastasia (DigitalOcean, Shellfish)
ssh root@159.65.43.12      # gematria  (DigitalOcean, Codex-Infinity)

# Via Tailscale
ssh root@100.94.33.37      # anastasia
ssh root@100.108.132.8     # gematria
```

### SSH Config Shortcuts

Add to `~/.ssh/config` for convenience:

```
Host cecilia
    HostName 192.168.4.89
    User pi

Host cecilia-ts
    HostName 100.72.180.98
    User pi

Host octavia
    HostName 192.168.4.38
    User pi

Host octavia-ts
    HostName 100.66.235.47
    User pi

Host alice
    HostName 192.168.4.49
    User alice

Host alice-ts
    HostName 100.77.210.18
    User alice

Host lucidia
    HostName 192.168.4.81
    User pi

Host lucidia-ts
    HostName 100.83.149.86
    User pi

Host aria
    HostName 192.168.4.82
    User pi

Host aria-ts
    HostName 100.109.14.17
    User pi

Host cordelia
    HostName 192.168.4.27
    User pi

Host anastasia
    HostName 174.138.44.45
    User root

Host anastasia-ts
    HostName 100.94.33.37
    User root

Host gematria
    HostName 159.65.43.12
    User root

Host gematria-ts
    HostName 100.108.132.8
    User root
```

---

## Ollama Endpoints

### Octavia (Primary Compute — Mercury, Hermes, Hestia)

```bash
# List models
curl http://192.168.4.38:11434/api/tags

# Generate (qwen2.5-coder:32b — Mercury)
curl -X POST http://192.168.4.38:11434/api/generate \
  -d '{"model": "qwen2.5-coder:32b", "prompt": "Hello", "stream": false}'

# Models available: qwen2.5-coder:32b, deepseek-coder:6.7b, mistral:7b
```

### Cecilia (CECE OS)

```bash
# List models
curl http://192.168.4.89:11434/api/tags

# Models available: qwen2.5:7b, deepseek-r1:7b, llama3.2:3b
```

---

## Roku Devices (ECP API)

Both Roku devices expose the External Control Protocol on port 8060.

```bash
# Pandora (Living Room TV)
curl http://192.168.4.26:8060/query/device-info

# Calliope (Streaming Stick on pandora)
curl http://192.168.4.33:8060/query/device-info

# List installed apps
curl http://192.168.4.26:8060/query/apps

# Launch an app (e.g., Netflix = 12)
curl -X POST http://192.168.4.26:8060/launch/12
```

---

## USB Devices (via alexandria)

USB peripherals are attached to the Mac M1 workstation.

### Siren (Sipeed BL808 RISC-V)

```bash
# Serial connection (2Mbaud)
screen /dev/tty.usbmodem* 2000000

# Check USB device
system_profiler SPUSBDataType | grep -A5 "Sipeed"
```

### Lyra (MIDI Interface)

```bash
# List MIDI devices (macOS)
system_profiler SPUSBDataType | grep -A5 "Kalezo"
```

### WaveCube (ESP32 + DLP2000 Projector)

```bash
# Serial connection (115200 baud)
screen /dev/tty.usbserial* 115200

# Check USB device
system_profiler SPUSBDataType | grep -A5 "CH340"
```

The WaveCube is a gutted wave lamp containing an ESP32 with touchscreen,
a TI DLP2000 LightCrafter projector (640x360, 20 lumens), and a Pi Zero 2W
driving the projector via DPI (GPIO).

### Pixel Office Bridge (WebSocket)

```bash
# Connect to the agent coordination bridge
wscat -c ws://192.168.4.28:8765
```

---

## Mobile Devices

### Athena (iPhone/iPad)

- AirPlay: port 7000
- lockdownd: port 62078
- IP: 192.168.4.27 (shares with cordelia)

---

## Cloudflare Tunnel

The tunnel runs on **cecilia** and exposes local services to the internet:

```bash
# Check tunnel status (on cecilia)
ssh pi@192.168.4.89 "cloudflared tunnel info blackroad"

# Tunnel ID: 52915859-da18-4aa6-add5-7bd9fcac2e0b
# Protocol: QUIC | Edge: dfw08 (Dallas)

# Routes
# agent.blackroad.ai  → localhost:8080
# api.blackroad.ai    → localhost:3000
```

---

## Health Check

Run the discover script to ping all registered devices:

```bash
./scripts/discover.sh
```
