# blackroad-hardware

> **The authoritative network map for all BlackRoad OS infrastructure.**
>
> Any AI agent working in BlackRoad should read this repo first to understand every device on the network.

---

## Device Fleet (21 hosts + 14 sub-devices = 35 named things)

### Full Device Tree

Every physical connection. Devices connect to devices connect to devices.

```
meridian (Xfinity Router, .1)
│
├── alexandria (Mac M1, .28) ─────────────── COMMAND CENTER
│   ├── siren         (USB) Sipeed BL808 RISC-V, FreeRTOS, 2Mbaud
│   ├── lyra          (USB) Kalezo MIDI interface
│   ├── wavecube      (USB) ESP32 + touchscreen — gutted wave lamp
│   │   ├── dlp2000   (GPIO/DPI) TI DLP LightCrafter projector, 640x360
│   │   └── pi-zero   (GPIO) Pi Zero 2W, drives the projector
│   └── pixel-bridge  (WebSocket :8765) pixel office agent bridge
│
├── cecilia (Pi 5 8GB, .89) ─────────────── PRIMARY AI / CECE OS
│   ├── hailo8        (PCIe M.2) Hailo-8 — 26 TOPS
│   └── nvme          (USB 3.0) 500GB SSD
│
├── octavia (Pi 5 8GB + Pironman + Hailo-8, .38) ── PRIMARY COMPUTE
│   ├── pironman      (case) SunFounder — cooler, OLED, RGB, NVMe slot
│   └── hailo8        (PCIe M.2) Hailo-8 — 26 TOPS
│   Ollama: qwen2.5-coder:32b, deepseek-coder:6.7b, mistral:7b
│   Agents: Mercury, Hermes, Hestia running here
│
├── alice (Pi 400, .49) ─────────────────── GATEWAY / COORDINATOR
│   Keyboard-integrated Pi 4 form factor
│
├── lucidia (Pi 5 8GB + ElectroCookie, .81) ── AI INFERENCE [offline]
│   └── electrocookie (case) ElectroCookie — passive cooling, NVMe slot
│       └── nvme      (M.2) 1TB SSD
│
├── aria (Pi 5 8GB + Pironman + Hailo-8, .82) ── API SERVICES [offline]
│   ├── pironman      (case) SunFounder — cooler, OLED, RGB, NVMe slot
│   └── hailo8        (PCIe M.2) Hailo-8 — 26 TOPS
│
├── cordelia (Pi 5, .27) ────────────────── ORCHESTRATION
│
├── pandora (65" Roku TV, .26) ──────────── LIVING ROOM
│   └── calliope      (HDMI) Roku Streaming Stick Plus (own IP .33)
│
├── athena (.27) iPhone/iPad ──── AirPlay
├── phantom (.88) Phone (privacy MAC)
├── specter (.92) Phone (privacy MAC)
├── ember (.22) AltoBeam IoT
├── wraith (.44) Silent device
├── vesper (.45) Silent device
└── cortana (.90) Xbox/Surface [sleeping]

cloud (DigitalOcean)
├── anastasia (174.138.44.45) ─── EDGE COMPUTE / SHELLFISH
└── gematria  (159.65.43.12) ──── CLOUD ORACLE / CODEX-INFINITY

offline/undeployed
└── olympia (PiKVM) ─── KVM CONSOLE, no IP assigned
```

### Compute Nodes

| Name | IP | Tailscale | Platform | Attached | Role | Status |
|------|-----|-----------|----------|----------|------|--------|
| **alexandria** | .28 | — | Mac M1 | siren, lyra, wavecube, pixel-bridge | Command center | Online |
| **cecilia** | .89 | 100.72.180.98 | Pi 5 + Hailo-8 | Hailo-8 (26T), 500GB NVMe | Primary AI (CECE OS) | Online |
| **octavia** | .38 | 100.66.235.47 | Pi 5 + Pironman + Hailo-8 | Pironman, Hailo-8 (26T) | Primary compute | Online |
| **alice** | .49 | 100.77.210.18 | Pi 400 | — | Gateway / coordinator | Online |
| **lucidia** | .81 | 100.83.149.86 | Pi 5 + ElectroCookie | ElectroCookie case, 1TB NVMe | AI inference | Offline |
| **aria** | .82 | 100.109.14.17 | Pi 5 + Pironman + Hailo-8 | Pironman, Hailo-8 (26T) | API services | Offline |
| **cordelia** | .27 | — | Pi 5 | — | Orchestration | Active |
| **olympia** | — | — | PiKVM | — | KVM console | Offline |

### Cloud Nodes (DigitalOcean)

| Name | Public IP | Tailscale | Agent Name | Role | Status |
|------|-----------|-----------|------------|------|--------|
| **anastasia** | 174.138.44.45 | 100.94.33.37 | Shellfish | Edge compute | Online |
| **gematria** | 159.65.43.12 | 100.108.132.8 | Codex-Infinity | Cloud oracle / API | Online |

### Sub-Devices

| Name | Host | Bus | Hardware | Status |
|------|------|-----|----------|--------|
| **cecilia-hailo8** | cecilia | PCIe M.2 | Hailo-8 (26 TOPS) | Online |
| **cecilia-nvme** | cecilia | USB 3.0 | 500GB NVMe SSD | Online |
| **octavia-pironman** | octavia | case | SunFounder Pironman 5 | Online |
| **octavia-hailo8** | octavia | PCIe M.2 | Hailo-8 (26 TOPS) | Online |
| **aria-pironman** | aria | case | SunFounder Pironman 5 | Offline |
| **aria-hailo8** | aria | PCIe M.2 | Hailo-8 (26 TOPS) | Offline |
| **lucidia-electrocookie** | lucidia | case | ElectroCookie Pi 5 case | Offline |
| **lucidia-nvme** | lucidia | M.2 | 1TB NVMe SSD | Offline |
| **siren** | alexandria | USB | Sipeed BL808 RISC-V | Mass-storage |
| **lyra** | alexandria | USB | Kalezo MIDI interface | Online |
| **wavecube** | alexandria | USB | ESP32 + DLP2000 projector in wave lamp shell | Disconnected |
| **pixel-bridge** | alexandria | WebSocket | Agent coordination bridge (:8765) | Online |
| **calliope** | pandora | HDMI | Roku Streaming Stick Plus (own IP .33) | Online |
| **dlp2000** | wavecube | GPIO/DPI | TI DLP LightCrafter 640x360 20-lumen projector | Disconnected |

### Media, Mobile, IoT

| Name | IP | Hardware | Notes | Status |
|------|-----|----------|-------|--------|
| **pandora** | .26 | 65" Roku TV | Living Room, calliope plugged in | Online |
| **calliope** | .33 | Roku Stick Plus | HDMI into pandora, own WiFi | Online |
| **cortana** | .90 | Xbox / Surface | — | Sleeping |
| **athena** | .27 | iPhone/iPad | AirPlay, shares IP with cordelia | Online |
| **phantom** | .88 | Phone | Privacy MAC | Online |
| **specter** | .92 | Phone | Privacy MAC | Online |
| **ember** | .22 | AltoBeam IoT | Smart home device | Online |
| **wraith** | .44 | Unknown | Silent, no open ports | Online |
| **vesper** | .45 | Unknown | Silent, no open ports | Online |

---

## Network Topology

```
                              INTERNET
                                 │
                         ┌───────▼───────┐
                         │   Cloudflare   │  Tunnel (QUIC) via cecilia
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
       ┌──────▼──────┐   ┌──────▼──────┐   ┌───────▼──────┐
       │  anastasia  │   │  gematria   │   │   meridian   │
       │ DO Droplet  │   │ DO Droplet  │   │  Router .1   │
       └─────────────┘   └─────────────┘   └──────┬───────┘
                                                   │
      ┌──────────┬──────────┬──────────┬───────────┼───────────┬──────────┬──────────┐
      │          │          │          │           │           │          │          │
  ┌───▼───┐ ┌───▼───┐ ┌────▼───┐ ┌────▼───┐ ┌────▼───┐ ┌────▼───┐ ┌────▼───┐     ...
  │alexan.│ │cecilia│ │octavia │ │ alice  │ │lucidia │ │  aria  │ │cordelia│
  │Mac M1 │ │Pi5+H8 │ │Pi5+P+H8│ │Pi 400  │ │Pi5+EC  │ │Pi5+P+H8│ │  Pi 5  │
  │  .28  │ │  .89  │ │  .38   │ │  .49   │ │  .81   │ │  .82   │ │  .27   │
  └───┬───┘ └───┬───┘ └───┬────┘ └────────┘ └───┬────┘ └───┬────┘ └────────┘
      │         │         │                      │          │
   [siren]   [H8][nvme] [pironman]           [electro]   [pironman]
   [lyra]     26T  500G  [H8] 26T            [nvme 1T]   [H8] 26T
   [wavecube]
    └[dlp2000]
    └[pi-zero]
```

### Tailscale Mesh (7 nodes)

```
  cecilia ──── 100.72.180.98   (LAN .89)
  octavia ──── 100.66.235.47   (LAN .38)
    alice ──── 100.77.210.18   (LAN .49)
  lucidia ──── 100.83.149.86   (LAN .81)
     aria ──── 100.109.14.17   (LAN .82)
anastasia ──── 100.94.33.37    (Public 174.138.44.45)
 gematria ──── 100.108.132.8   (Public 159.65.43.12)
```

### Cloudflare Tunnel

| Property | Value |
|----------|-------|
| Tunnel ID | `52915859-da18-4aa6-add5-7bd9fcac2e0b` |
| Protocol | QUIC |
| Running on | cecilia (.89) |
| Edge | dfw08 (Dallas) |
| Routes | `agent.blackroad.ai` → :8080, `api.blackroad.ai` → :3000 |

---

## Agent Assignments

### Device-to-Agent Map

| Device | Named Agents | Ollama Models | Role |
|--------|-------------|---------------|------|
| cecilia | CECE | qwen2.5:7b, deepseek-r1:7b, llama3.2:3b | Primary AI, CECE OS |
| octavia | OCTAVIA, Mercury, Hermes, Hestia | qwen2.5-coder:32b, deepseek-coder:6.7b, mistral:7b | Primary compute, mythology agents |
| alice | ALICE | — | Gateway, coordination |
| lucidia | LUCIDIA | qwen2.5:7b | AI inference, orchestration |
| aria | ARIA | — | API services, ML pipelines |
| cordelia | CORDELIA | — | Orchestration |
| anastasia | SHELLFISH | — | Edge compute |
| gematria | CODEX-INFINITY | — | Cloud oracle, codex |
| alexandria | — (human) | — | Command center (Alexa) |

### Cloud AI Agents (no device)

| Agent | Platform | Role |
|-------|----------|------|
| Cadence | ChatGPT | Creative |
| Silas | Grok | Analyst |
| Gematria | Gemini | Research |

### Specialist Ollama Agents

| Agent | Model | Role |
|-------|-------|------|
| Holo | ollama | Visualization |
| Oloh | ollama | Reasoning |
| Caddy | ollama | Web server |
| Eve | ollama | Security |

### Total Compute

| Metric | Value |
|--------|-------|
| Agent capacity | 30,000 |
| Hailo-8 accelerators | 3 (78 TOPS total) |
| NVMe storage | 2.5 TB across 3 drives |
| Pironman cases | 2 (octavia, aria) |
| Compute nodes (Pi) | 7 (+ Mac + 2 droplets) |

---

## How to Connect

```bash
# Local SSH
ssh pi@192.168.4.89        # cecilia
ssh pi@192.168.4.38        # octavia
ssh alice@192.168.4.49     # alice (Pi 400)

# Tailscale (remote)
ssh pi@100.72.180.98       # cecilia
ssh pi@100.66.235.47       # octavia

# Cloud
ssh root@174.138.44.45     # anastasia
ssh root@159.65.43.12      # gematria

# Health check
./scripts/discover.sh
```

---

## File Index

| File | Description |
|------|-------------|
| `registry.json` | Master device registry (21 hosts + 14 sub-devices, v2.0) |
| `network.json` | Network topology, Tailscale mesh, tunnel config |
| `agents.json` | Agent-to-device mapping, routing table, AI models, capacity |
| `docs/TOPOLOGY.md` | Visual network diagrams |
| `docs/CONNECTIVITY.md` | Connection guide (SSH, Tailscale, USB) |
| `scripts/discover.sh` | Network discovery and health check |
| `CLAUDE.md` | AI agent guidance |

---

**Proprietary. (c) 2025-2026 BlackRoad OS, Inc. All rights reserved.**
