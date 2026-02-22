# blackroad-hardware

> Hardware fleet registry, network topology, device manifests, and management scripts for BlackRoad OS infrastructure.

[![CI](https://github.com/BlackRoad-OS-Inc/blackroad-hardware/actions/workflows/ci.yml/badge.svg)](https://github.com/BlackRoad-OS-Inc/blackroad-hardware/actions/workflows/ci.yml)

## Overview

Single source of truth for all physical hardware in the BlackRoad OS fleet — Raspberry Pi cluster, DigitalOcean droplets, XR headsets, accelerators, MCU array, and network topology.

**22 devices** across 7 tiers.

## Structure

```
blackroad-hardware/
├── fleet-registry.yaml    # Source of truth — all devices (YAML)
├── registry.json          # Legacy device registry (JSON)
├── network.json           # Network topology & IP assignments
├── devices/               # Per-device-type documentation
│   ├── raspberry-pi.md    # Pi cluster setup + services
│   ├── edge-compute.md    # Jetson + RISC-V
│   ├── cloud-compute.md   # DigitalOcean droplets
│   ├── xr-headsets.md     # Meta Quest 2 (andromeda)
│   ├── consumer-devices.md
│   ├── iot-sensors.md
│   └── microcontrollers.md
├── accelerators/          # GPU/AI accelerator configs (Hailo-8, M1 NE)
├── network/               # Network diagrams & WireGuard configs
├── monitoring/            # Health check scripts
├── docs/                  # Hardware documentation
└── scripts/               # Fleet management scripts
    ├── fleet-health-check.sh
    ├── hardware-inventory.sh
    └── quest-adb.sh       # Meta Quest 2 (andromeda) ADB manager
```

## Fleet Summary

### Production Pi Cluster

| Name | IP | Role | Notes |
|------|-----|------|-------|
| cecilia | 192.168.4.89 | Primary AI host | Hailo-8 26 TOPS, NVMe |
| octavia | 192.168.4.38 | AI inference, auth, DNS | Pironman case |
| lucidia | 192.168.4.81 | NATS bus, LLM inference | Overclocked 2.6GHz |
| aria | 192.168.4.82 | API services, compute | |
| anastasia | 192.168.4.33 | AI inference secondary | SSH closed |
| cordelia | 192.168.4.27 | Orchestration | |
| alice | 192.168.4.49 | Gateway, development | Pi 400 keyboard |
| olympia | — | KVM console | Pi 4B, offline |

### Cloud

| Name | IP | Role |
|------|-----|------|
| codex-infinity | 159.65.43.12 | Codex server, oracle |
| shellfish | 174.138.44.45 | WireGuard hub, cloud infra |

### XR

| Name | Model | Role | Status |
|------|-------|------|--------|
| andromeda | Meta Quest 2 | XR interface, spatial agent | setup_pending |

### Key Specs
- **AI TOPS (confirmed):** 41.8 (Hailo-8 + M1 Neural Engine)
- **Network:** WireGuard hub-and-spoke, Cloudflare tunnels
- **Agents:** 30,000 capacity across Pi cluster

## Quick Start

```bash
# Check fleet health
./scripts/fleet-health-check.sh

# Manage Meta Quest 2
./scripts/quest-adb.sh devices         # detect Quest
./scripts/quest-adb.sh wifi-enable     # enable WiFi ADB
./scripts/quest-adb.sh status          # hardware info
./scripts/quest-adb.sh bootstrap-agents  # install BlackRoad agents
```

## Key Files

- `fleet-registry.yaml` — All 22 devices with full specs, IPs, roles, services
- `devices/xr-headsets.md` — Quest 2 setup, ADB guide, Termux agent bootstrap
- `devices/raspberry-pi.md` — Pi cluster services and setup

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

© BlackRoad OS, Inc. — All rights reserved. Proprietary.
