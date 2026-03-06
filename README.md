# blackroad-hardware

> Hardware fleet registry, network topology, device manifests, and management scripts for BlackRoad OS infrastructure.

[![CI](https://github.com/BlackRoad-OS-Inc/blackroad-hardware/actions/workflows/ci.yml/badge.svg)](https://github.com/BlackRoad-OS-Inc/blackroad-hardware/actions/workflows/ci.yml)

## Overview

Single source of truth for all physical hardware in the BlackRoad OS fleet — Raspberry Pi cluster, DigitalOcean droplets, XR headsets, AI accelerators, MCU array, and network topology.

**22 devices** across 7 tiers | **67.8 TOPS** confirmed AI compute | **30,000** agent capacity

## Structure

```
blackroad-hardware/
├── fleet-registry.yaml    # Source of truth — all devices (YAML)
├── registry.json          # Device registry (JSON, 22 devices)
├── network.json           # Network topology & IP assignments
├── CLAUDE.md              # AI agent instructions
├── src/
│   └── fleet_manager.py   # Python fleet orchestration library
├── tests/
│   └── test_hardware.py   # Fleet manager + schema validation tests
├── devices/               # Per-device-type documentation
│   ├── raspberry-pi.md    # Pi cluster (8 nodes) setup + services
│   ├── edge-compute.md    # Jetson Orin Nano + RISC-V
│   ├── cloud-compute.md   # DigitalOcean droplets
│   ├── xr-headsets.md     # Meta Quest 2 (andromeda)
│   ├── consumer-devices.md
│   ├── iot-sensors.md     # Sensors + I2C device map
│   └── microcontrollers.md # 21 MCU units across 9 types
├── accelerators/
│   └── ai-compute.md      # Hailo-8, Jetson, M1 Neural Engine
├── network/               # Network diagrams & WireGuard configs
│   ├── topology.md        # Physical LAN, WireGuard mesh, tunnels
│   ├── services-map.md    # Service routing and port mappings
│   └── topology.yaml
├── projects/
│   └── wavecube/          # WaveCube hologram projector
├── docs/
│   ├── CONNECTIVITY.md    # SSH, Ollama, API endpoints
│   └── TOPOLOGY.md        # Device tree & subnet map
└── scripts/
    ├── discover.sh            # Network device discovery
    ├── fleet-health-check.sh  # Comprehensive fleet health monitor
    ├── hardware-inventory.sh  # Agent registry query tool
    ├── pi-deploy.sh           # Deploy code to Pis via rsync
    ├── pi-health-monitor.sh   # Per-node metrics collector
    ├── quest-adb.sh           # Meta Quest 2 ADB manager
    └── quest-bootstrap.sh     # Quest agent bootstrap
```

## Fleet Summary

### Production Pi Cluster (8 nodes)

| Name | IP | WireGuard | Role | Accelerator | Status |
|------|-----|-----------|------|-------------|--------|
| cecilia | 192.168.4.89 | 10.8.0.3 | Primary AI host | Hailo-8 (26 TOPS) | online |
| octavia | 192.168.4.38 | — | AI inference, auth, DNS | — | online |
| lucidia | 192.168.4.81 | 10.8.0.4 | NATS bus, LLM inference | Hailo-8 (26 TOPS) | online |
| aria | 192.168.4.82 | 10.8.0.7 | API services, compute | — | online |
| anastasia | 192.168.4.33 | — | AI inference secondary | — | online |
| cordelia | 192.168.4.27 | — | Orchestration | — | online |
| alice | 192.168.4.49 | 10.8.0.6 | Gateway, development | — | online |
| olympia | — | — | KVM console | — | offline |

### Cloud (2 DigitalOcean droplets)

| Name | Public IP | Role |
|------|-----------|------|
| codex-infinity (gematria) | 159.65.43.12 | Codex server, oracle |
| shellfish (anastasia) | 174.138.44.45 | WireGuard hub (10.8.0.1), cloud infra |

### Edge Compute

| Name | Hardware | Role | Status |
|------|----------|------|--------|
| jetson-agent | NVIDIA Orin Nano (40 TOPS) | Edge AI inference | pending |
| persephone | Sipeed RISC-V | Portable compute | active |

### XR

| Name | Model | Role | Status |
|------|-------|------|--------|
| andromeda | Meta Quest 2 (Snapdragon XR2) | XR interface, spatial agent | setup_pending |

### AI Compute

| Accelerator | TOPS | Node | Status |
|-------------|------|------|--------|
| Hailo-8 M.2 | 26 | cecilia | active |
| Hailo-8 M.2 | 26 | lucidia | active |
| M1 Neural Engine | 15.8 | alexandria (Mac) | active |
| Jetson Orin Nano | 40 | jetson-agent | pending |
| **Total confirmed** | **67.8** | | |

### Microcontrollers (21 units)

- **ESP32 family (13):** SuperMini (5), N8R8 (2), touchscreen (3), Heltec LoRa (1), M5Stack Atom (2)
- **Arduino family (5):** ELEGOO UNO R3 (2), ATTINY88 (3)
- **Other (3):** Pico RP2040 (2), WCH CH32V003 (1)

### Network

- **LAN:** 192.168.4.0/24 via TP-Link router
- **WireGuard:** Hub-and-spoke via Shellfish (10.8.0.0/24)
- **Cloudflare tunnels:** 5 active (cecilia, octavia, codex, cadence; lucidia down)
- **DNS:** PowerDNS on Octavia, Cloudflare CDN for blackroad.io
- **Ollama endpoints:** Octavia (primary), Cecilia (secondary)

## Quick Start

```bash
# Check fleet health
./scripts/fleet-health-check.sh

# Discover all network devices
./scripts/discover.sh

# Hardware inventory
./scripts/hardware-inventory.sh
./scripts/hardware-inventory.sh --live    # with ping scan
./scripts/hardware-inventory.sh --json    # JSON output

# SSH to a Pi
ssh pi@192.168.4.89          # cecilia
ssh pi@192.168.4.38          # octavia
ssh alice@192.168.4.49       # alice

# SSH via WireGuard (remote)
ssh pi@10.8.0.3              # cecilia
ssh pi@10.8.0.4              # lucidia

# Manage Meta Quest 2
./scripts/quest-adb.sh devices
./scripts/quest-adb.sh wifi-enable
./scripts/quest-adb.sh status
./scripts/quest-adb.sh bootstrap-agents

# Deploy to Pi fleet
./scripts/pi-deploy.sh all
./scripts/pi-deploy.sh cecilia

# Run tests
pip install -r requirements.txt
pytest tests/ -v
```

## Key Files

| File | Purpose |
|------|---------|
| `fleet-registry.yaml` | All 22 devices with full specs, IPs, roles, services |
| `registry.json` | Device registry (JSON format, 22 devices) |
| `network.json` | Network topology, subnets, Ollama endpoints |
| `src/fleet_manager.py` | Python fleet orchestration (PiNode, FleetRegistry, SensorReading) |
| `devices/raspberry-pi.md` | Pi cluster services, SSH access, errata |
| `devices/xr-headsets.md` | Quest 2 setup, ADB guide, Termux agent bootstrap |
| `accelerators/ai-compute.md` | AI accelerator specs, model compatibility, power efficiency |
| `network/topology.md` | Physical LAN, WireGuard mesh, Cloudflare tunnels |

## Roadmap

### Active — Pi Cluster Agent Deployment
Deploy Ollama and agent runtime across all 4 target Pi nodes (blackroad-pi, aria64, alice, lucidia) with systemd auto-restart and mesh monitoring integration.

### Active — Fleet Manifest & Inventory
Authoritative hardware inventory JSON for all Pi nodes with WireGuard IPs. Schema validated in CI, synchronized with README.

### Planned — RS485 Industrial Sensor Mesh
RS485 multi-drop bus connecting MCUs and sensors via Modbus RTU protocol with Pi-to-RS485 bridge and agent drivers.

### Planned — Universal Video Mesh (UVM)
Distributed display grid where each node renders agent activity and dashboards with orchestration protocol.

### Planned — Hologram Control Center
Pepper's Ghost holographic display integration for physically manifesting agent output via display renderer.

### Planned — Jetson Orin Nano Setup
Boot Jetson hardware, install JetPack SDK, deploy Ollama with GPU inference, run benchmarks, integrate into agent mesh.

### Planned — Macro-Quantum Sentinel
Advanced compute infrastructure integration with Zero-Hop tunnel configuration.

### Future — Hologram Cellular Modem
Cellular fallback connectivity via Hologram for Pi fleet network resilience with auto-failover and signal monitoring.

## CI

CI runs on GitHub Actions (`ubuntu-latest`) with three jobs:

1. **Lint & Validate** — Secret scanning, YAML/JSON validation
2. **Python Tests** — pytest against `fleet_manager.py` and schema validation
3. **Fleet Schema Validation** — Validates `fleet-registry.yaml` and `registry.json`

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

© BlackRoad OS, Inc. — All rights reserved. Proprietary.
