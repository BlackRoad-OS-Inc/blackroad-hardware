# blackroad-hardware

> **The authoritative network map for all BlackRoad OS infrastructure.**
>
> Any AI agent working in BlackRoad should read this repo first to understand every device on the network.

---

## Device Fleet (22 named devices + 6 sub-devices)

### Device Tree

Every physical connection at a glance. Devices connect to devices.

```
meridian (Xfinity Router, .1)
├── alexandria (Mac M1, .28) ─── COMMAND CENTER
│   ├── siren       (USB) Sipeed BL808 RISC-V
│   ├── lyra        (USB) Kalezo MIDI interface
│   └── wavecube    (USB) ESP32 + touchscreen, BlackRoad OS Enhanced v2.0
│
├── cecilia (Pi 5, .89) ─── PRIMARY AI AGENT / CECE OS
│   ├── hailo8      (PCIe/M.2) Hailo-8 AI Accelerator — 26 TOPS
│   └── cecilia-nvme (USB 3.0) 500GB NVMe SSD
│
├── octavia (Pi 5, .38) ─── PRIMARY COMPUTE
├── alice (Pi 4, .49) ─── WORKER / COORDINATOR
│
├── lucidia (Pi 5, .81) ─── AI INFERENCE [offline]
│   └── pironman    (case) SunFounder Pironman 5 — cooler, OLED, RGB, NVMe slot
│       └── lucidia-nvme (M.2) 1TB NVMe SSD
│
├── aria (Pi 5, .82) ─── DATA SCIENCE [offline]
│
├── pandora (65" Roku TV, .26) ─── LIVING ROOM
│   └── calliope    (HDMI) Roku Streaming Stick Plus
│
├── athena (.27) iPhone/iPad
├── phantom (.88) Phone (privacy MAC)
├── specter (.92) Phone (privacy MAC)
├── ember (.22) AltoBeam IoT
├── wraith (.44) Silent device
├── vesper (.45) Silent device
└── cortana (.90) Xbox/Surface [sleeping]

cloud (DigitalOcean)
├── anastasia (174.138.44.45) ─── EDGE COMPUTE
└── gematria  (159.65.43.12) ─── CLOUD ORACLE
```

### Compute Nodes

| Name | IP | Tailscale | Hardware | Attached | Role | Status |
|------|-----|-----------|----------|----------|------|--------|
| **alexandria** | .28 | — | Mac M1 | siren, lyra, wavecube (USB) | Command center | Online |
| **cecilia** | .89 | 100.72.180.98 | Pi 5 | Hailo-8 (26 TOPS), 500GB NVMe | Primary AI agent | Online |
| **octavia** | .38 | 100.66.235.47 | Pi 5 | — | Primary compute | Online |
| **alice** | .49 | 100.77.210.18 | Pi 4 | — | Worker / coordinator | Online |
| **lucidia** | .81 | 100.83.149.86 | Pi 5 | Pironman case, 1TB NVMe | AI inference | Offline |
| **aria** | .82 | 100.109.14.17 | Pi 5 | — | Data science | Offline |

### Cloud Nodes (DigitalOcean)

| Name | Public IP | Tailscale | Role | Status |
|------|-----------|-----------|------|--------|
| **anastasia** | 174.138.44.45 | 100.94.33.37 | Edge compute (Shellfish) | Online |
| **gematria** | 159.65.43.12 | 100.108.132.8 | Cloud oracle / API | Online |

### Sub-Devices (attached to hosts)

| Name | Host | Connection | Hardware | Status |
|------|------|------------|----------|--------|
| **hailo8** | cecilia | PCIe M.2 | Hailo-8 AI Accelerator (26 TOPS) | Online |
| **cecilia-nvme** | cecilia | USB 3.0 | 500GB NVMe SSD | Online |
| **pironman** | lucidia | case | SunFounder Pironman 5 (cooler, OLED, NVMe slot) | Online |
| **lucidia-nvme** | lucidia | M.2 via Pironman | 1TB NVMe SSD | Offline |
| **siren** | alexandria | USB | Sipeed BL808 RISC-V (FreeRTOS) | Mass-storage |
| **lyra** | alexandria | USB | Kalezo MIDI interface | Online |
| **wavecube** | alexandria | USB | ESP32 + touchscreen (BlackRoad OS Enhanced) | Disconnected |
| **calliope** | pandora | HDMI | Roku Streaming Stick Plus 3830R | Online |

### Media & Entertainment

| Name | IP | Hardware | Location | Status |
|------|-----|----------|----------|--------|
| **pandora** | .26 | 65" Roku TV (65R4CX) | Living Room | Online |
| **calliope** | .33 | Roku Stick Plus (plugged into pandora) | Bedroom | Online |
| **cortana** | .90 | Xbox / Surface | — | Sleeping |

### Mobile Devices

| Name | IP | Hardware | Status |
|------|-----|----------|--------|
| **athena** | .27 | iPhone/iPad (AirPlay) | Online |
| **phantom** | .88 | Phone (privacy MAC) | Online |
| **specter** | .92 | Phone (privacy MAC) | Online |

### IoT & Unknown

| Name | IP | Vendor | Description | Status |
|------|-----|--------|-------------|--------|
| **ember** | .22 | AltoBeam | Smart home IoT | Online |
| **wraith** | .44 | Private | Silent, no open ports | Online |
| **vesper** | .45 | Private | Silent, no open ports | Online |

---

## Network Topology

```
                              INTERNET
                                 │
                         ┌───────▼───────┐
                         │   Cloudflare   │  CDN, DNS, Tunnel (QUIC)
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
       ┌──────▼──────┐   ┌──────▼──────┐   ┌───────▼──────┐
       │  anastasia  │   │  gematria   │   │   meridian   │
       │ DO Droplet  │   │ DO Droplet  │   │  Router .1   │
       └─────────────┘   └─────────────┘   └──────┬───────┘
                                                   │
              ┌──────────┬─────────┬───────────────┼─────────────┬──────────┐
              │          │         │               │             │          │
       ┌──────▼──┐ ┌─────▼───┐ ┌──▼─────┐  ┌─────▼────┐ ┌─────▼───┐ ┌────▼───┐
       │alexandria│ │ cecilia │ │octavia │  │  alice   │ │ lucidia │ │  aria  │
       │ Mac M1  │ │  Pi 5   │ │  Pi 5  │  │  Pi 4   │ │  Pi 5   │ │  Pi 5  │
       │  .28    │ │  .89    │ │  .38   │  │  .49    │ │  .81    │ │  .82   │
       └────┬────┘ └────┬────┘ └────────┘  └─────────┘ └────┬────┘ └────────┘
            │            │                                    │
     ┌──────┼──────┐  ┌──┴────────┐                    ┌─────┴─────┐
     │      │      │  │           │                    │           │
  [siren] [lyra] [wave│ [hailo8]  │ [nvme]         [pironman]     │
   RISC-V  MIDI  cube │  26 TOPS  │ 500GB            case      [nvme]
                      │  PCIe     │ USB 3            OLED       1TB
                      │           │                  M.2 slot
```

### Tailscale Mesh (7 nodes)

All compute and cloud nodes connected via Tailscale for remote access:

```
  cecilia ──── 100.72.180.98
  octavia ──── 100.66.235.47
    alice ──── 100.77.210.18
  lucidia ──── 100.83.149.86
     aria ──── 100.109.14.17
anastasia ──── 100.94.33.37   (DigitalOcean)
 gematria ──── 100.108.132.8  (DigitalOcean)
```

### Cloudflare Tunnel

| Property | Value |
|----------|-------|
| Tunnel ID | `52915859-da18-4aa6-add5-7bd9fcac2e0b` |
| Protocol | QUIC |
| Running on | cecilia (192.168.4.89) |
| Edge | dfw08 (Dallas) |
| Routes | `agent.blackroad.ai` → :8080, `api.blackroad.ai` → :3000 |

---

## Agent Assignments

| Device | Named Agent | Specialization |
|--------|-------------|----------------|
| cecilia | CECE | CECE OS, 68 sovereign apps, Hailo-8 edge AI |
| octavia | OCTAVIA | ML acceleration, 22,500 agent capacity |
| alice | ALICE | Agent coordination, distributed systems |
| lucidia | LUCIDIA | Multi-agent orchestration, NLU |
| aria | ARIA | ML pipelines, data science |
| anastasia | SHELLFISH | Edge compute, failover |
| alexandria | — | Human orchestrator (Alexa) |

### Total AI Compute

| Metric | Value |
|--------|-------|
| Total agent capacity | 30,000 |
| AI research agents | 12,592 |
| Code deploy agents | 8,407 |
| Infrastructure agents | 5,401 |
| Monitoring agents | 3,600 |
| Edge AI (Hailo-8) | 26 TOPS |

---

## How to Connect

```bash
# Local SSH
ssh pi@192.168.4.89        # cecilia
ssh pi@192.168.4.38        # octavia
ssh alice@192.168.4.49     # alice

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
| `registry.json` | Master device registry (22 devices, full specs) |
| `network.json` | Network topology, Tailscale mesh, tunnel config |
| `agents.json` | Agent-to-device mapping, AI models, capacity |
| `docs/TOPOLOGY.md` | Visual network diagrams |
| `docs/CONNECTIVITY.md` | Connection guide (SSH, Tailscale, USB) |
| `scripts/discover.sh` | Network discovery and health check |
| `CLAUDE.md` | AI agent guidance |

---

**Proprietary. (c) 2025-2026 BlackRoad OS, Inc. All rights reserved.**
