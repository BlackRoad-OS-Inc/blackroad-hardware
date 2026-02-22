# blackroad-hardware

> Hardware fleet registry, network topology, and device manifests for BlackRoad OS infrastructure.

[![CI](https://github.com/BlackRoad-OS-Inc/blackroad-hardware/actions/workflows/ci.yml/badge.svg)](https://github.com/BlackRoad-OS-Inc/blackroad-hardware/actions/workflows/ci.yml)

## Overview

Single source of truth for all physical hardware in the BlackRoad OS fleet — Raspberry Pis, DigitalOcean droplets, accelerators, and network topology.

## Structure

```
blackroad-hardware/
├── registry.json          # Master device registry
├── network.json           # Network topology & IP assignments
├── fleet-registry.yaml    # Fleet manifest (YAML)
├── devices/               # Per-device configuration
├── accelerators/          # GPU/AI accelerator configs
├── network/               # Network diagrams & configs
├── monitoring/            # Health check scripts
├── docs/                  # Hardware documentation
└── scripts/               # Fleet management scripts
```

## Fleet Summary

| Device | IP | Role | Capacity |
|--------|-----|------|----------|
| blackroad-pi (octavia) | 192.168.4.64 | Primary — Cloudflare tunnel | 22,500 agents |
| aria64 (lucidia) | 192.168.4.38 | Secondary — AI accelerator | 7,500 agents |
| alice | 192.168.4.49 | Tertiary | — |
| blackroad os-infinity (DO) | 159.65.43.12 | Cloud droplet | — |

## Key Files

- `registry.json` — All devices with specs, IPs, roles
- `network.json` — Network topology, subnets, DNS
- `fleet-registry.yaml` — Kubernetes-style fleet manifest

## Scripts

```bash
./scripts/fleet-health-check.sh    # Ping all devices
./scripts/hardware-inventory.sh    # Generate inventory report
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

---

© BlackRoad OS, Inc. — All rights reserved. Proprietary.
