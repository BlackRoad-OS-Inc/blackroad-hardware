# Network Topology

## Full Device Tree

Every device-connected-to-device relationship in the fleet.

```
meridian (Xfinity Router, 192.168.4.1)
│
├─── alexandria (Mac M1, .28) ──────────── COMMAND CENTER
│    ├── siren        USB  Sipeed BL808 RISC-V  [mass-storage]
│    │                     FreeRTOS/POSIX, 2Mbaud serial
│    │                     WiFi, OTA, UDP broadcast, DMA video
│    ├── lyra         USB  Kalezo MIDI interface  [online]
│    │                     WaveQube MIDI controller
│    ├── wavecube     USB  QinHeng CH340 / ESP32 + touchscreen  [disconnected]
│    │                     BlackRoad OS Enhanced v2.0
│    │                     8 apps: dashboard, weather, crypto, browser,
│    │                     snake, network, settings, portfolio
│    │   ├── dlp2000  GPIO/DPI  TI DLP LightCrafter  [disconnected]
│    │   │                      640x360, 20-lumen projector
│    │   │                      MickMake PCB adapter, RGB666 18-bit
│    │   └── pi-zero  GPIO      Pi Zero 2W  [disconnected]
│    │                          Drives DLP2000 via DPI, gpu_mem=64
│    └── pixel-bridge WebSocket Agent coordination bridge (:8765)  [online]
│
├─── cecilia (Pi 5 8GB, .89) ──────────── PRIMARY AI / CECE OS
│    │   Tailscale: 100.72.180.98
│    │   Services: cece-os, ollama, cloudflared
│    │   Models: qwen2.5:7b, deepseek-r1:7b, llama3.2:3b
│    ├── hailo8       PCIe/M.2  Hailo-8 AI Accelerator  [online]
│    │                          26 TOPS neural network inference
│    │                          M.2 key-M via Pi 5 HAT
│    └── cecilia-nvme USB 3.0   500GB NVMe SSD  [online]
│                               Primary storage for CECE OS + models
│
├─── octavia (Pi 5 8GB + Pironman + Hailo-8, .38) ── PRIMARY COMPUTE
│    │   Tailscale: 100.66.235.47
│    │   Services: ollama, agent-runtime
│    │   Models: qwen2.5-coder:32b, deepseek-coder:6.7b, mistral:7b
│    │   Agents: Mercury, Hermes, Hestia
│    │   Agent capacity: 22,500
│    ├── pironman     case  SunFounder Pironman 5  [online]
│    │                      Active cooling (ICE Tower)
│    │                      OLED status display, RGB LED fan
│    │                      Safe shutdown button, M.2 NVMe slot
│    └── hailo8       PCIe/M.2  Hailo-8 AI Accelerator  [online]
│                               26 TOPS neural network inference
│
├─── alice (Pi 400, .49) ──────────────── GATEWAY / COORDINATOR
│        Tailscale: 100.77.210.18
│        Services: agent-management, coordination
│        Keyboard-integrated Pi 4 form factor
│
├─── lucidia (Pi 5 8GB + ElectroCookie, .81) ── AI INFERENCE [offline]
│    │   Tailscale: 100.83.149.86
│    │   Services: ollama, agent-orchestration
│    │   Models: qwen2.5:7b
│    │   Agent capacity: 7,500
│    └── electrocookie case  ElectroCookie Pi 5 case  [offline]
│        │                   Passive cooling, built-in M.2 NVMe slot
│        └── lucidia-nvme  M.2  1TB NVMe SSD  [offline]
│                               Mounted through ElectroCookie's M.2 slot
│
├─── aria (Pi 5 8GB + Pironman + Hailo-8, .82) ── API SERVICES [offline]
│    │   Tailscale: 100.109.14.17
│    │   Services: ml-pipelines, data-analysis, api-services
│    ├── pironman     case  SunFounder Pironman 5  [offline]
│    │                      Active cooling (ICE Tower)
│    │                      OLED status display, RGB LED fan
│    │                      Safe shutdown button, M.2 NVMe slot
│    └── hailo8       PCIe/M.2  Hailo-8 AI Accelerator  [offline]
│                               26 TOPS neural network inference
│
├─── cordelia (Pi 5, .27) ─────────────── ORCHESTRATION
│        Services: orchestration
│
├─── pandora (65" Roku TV, .26) ─────────── LIVING ROOM
│    └── calliope     HDMI  Roku Streaming Stick Plus 3830R  [online]
│                           Has own network IP: .33
│                           API: http://192.168.4.33:8060
│
├─── athena (.27)  iPhone/iPad ───────────── AirPlay + lockdownd
├─── phantom (.88) Phone (randomized MAC)
├─── specter (.92) Phone (randomized MAC)
├─── ember (.22)   AltoBeam IoT device
├─── wraith (.44)  Silent, no ports
├─── vesper (.45)  Silent, no ports
└─── cortana (.90) Xbox/Surface [sleeping]


CLOUD (DigitalOcean, not on LAN)
├── anastasia (174.138.44.45) ─── EDGE COMPUTE / SHELLFISH
│       Tailscale: 100.94.33.37
│       Services: edge-compute, agent-runtime
└── gematria  (159.65.43.12) ──── CLOUD ORACLE / CODEX-INFINITY
        Tailscale: 100.108.132.8
        Services: websocket, api, mining, codex

OFFLINE / UNDEPLOYED
└── olympia (PiKVM) ─── KVM CONSOLE, no IP assigned
```

## Physical Network Layout

```
                              INTERNET
                                 │
                         ┌───────▼───────┐
                         │   Cloudflare   │
                         │  Tunnel (QUIC) │
                         │  via cecilia   │
                         └───────┬───────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
       ┌──────▼──────┐   ┌──────▼──────┐   ┌───────▼──────┐
       │  anastasia  │   │  gematria   │   │   meridian   │
       │ DO NYC      │   │ DO NYC      │   │  Xfinity GW  │
       │ 174.138.44  │   │ 159.65.43   │   │  .1          │
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
    ├[dlp2000]
    └[pi-zero]
```

## Tailscale Mesh Overlay (7 nodes)

```
  cecilia ──── 100.72.180.98   (LAN .89)
  octavia ──── 100.66.235.47   (LAN .38)
    alice ──── 100.77.210.18   (LAN .49)
  lucidia ──── 100.83.149.86   (LAN .81)
     aria ──── 100.109.14.17   (LAN .82)
anastasia ──── 100.94.33.37    (Public 174.138.44.45)
 gematria ──── 100.108.132.8   (Public 159.65.43.12)
```

## Subnet Map (192.168.4.0/24)

```
  .1   meridian     Router (gateway)
  .22  ember        IoT (AltoBeam)
  .26  pandora      TV (65" Roku) ← calliope plugged in via HDMI
  .27  cordelia     Pi 5 (orchestration) — athena (iPhone) shares this IP
  .28  alexandria   Workstation (Mac M1) ← siren, lyra, wavecube via USB
  .33  calliope     Streaming (Roku Stick, physically on pandora)
  .38  octavia      Pi 5 + Pironman + Hailo-8 (primary compute)
  .44  wraith       Unknown (silent)
  .45  vesper       Unknown (silent)
  .49  alice        Pi 400 (gateway/coordinator)
  .81  lucidia      Pi 5 + ElectroCookie (AI inference) ← 1TB NVMe
  .82  aria         Pi 5 + Pironman + Hailo-8 (API services)
  .88  phantom      Mobile (privacy MAC)
  .89  cecilia      Pi 5 + Hailo-8 (CECE OS) ← 500GB NVMe
  .90  cortana      Console (Xbox/Surface)
  .92  specter      Mobile (privacy MAC)
```

## Device Count

```
  Compute hosts (8)  ████████████████████████  alexandria, cecilia, octavia, alice, lucidia, aria, cordelia, olympia
  Sub-devices (14)   ██████████████████████████████████████  3× hailo8, 2× nvme, 2× pironman, electrocookie,
                                                             siren, lyra, wavecube, pixel-bridge, calliope, dlp2000
  Cloud (2)          ██████                        anastasia, gematria
  Media (2)          ██████                        pandora, cortana
  Mobile (3)         █████████                     athena, phantom, specter
  IoT (1)            ███                           ember
  Unknown (2)        ██████                        wraith, vesper
  Router (1)         ███                           meridian
  ─────────────────────────────────────────────────
  Total:  33 (21 hosts + 14 sub-devices — 2 shared = 33 unique IPs/names)
```
