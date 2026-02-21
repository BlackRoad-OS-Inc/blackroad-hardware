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
│    └── wavecube     USB  QinHeng CH340 / ESP32 + touchscreen  [disconnected]
│                          BlackRoad OS Enhanced v2.0
│                          8 apps: dashboard, weather, crypto, browser,
│                          snake, network, settings, portfolio
│
├─── cecilia (Pi 5 8GB, .89) ──────────── PRIMARY AI AGENT
│    │   Tailscale: 100.72.180.98
│    │   Services: cece-os, ollama, cloudflared
│    ├── hailo8       PCIe/M.2  Hailo-8 AI Accelerator  [online]
│    │                          26 TOPS neural network inference
│    │                          M.2 key-M via Pi 5 HAT
│    └── cecilia-nvme USB 3.0   500GB NVMe SSD  [online]
│                               Primary storage for CECE OS + models
│
├─── octavia (Pi 5, .38) ──────────────── PRIMARY COMPUTE
│        Tailscale: 100.66.235.47
│        Services: ollama, agent-runtime
│        Agent capacity: 22,500
│
├─── alice (Pi 4, .49) ────────────────── WORKER / COORDINATOR
│        Tailscale: 100.77.210.18
│        Services: agent-management, coordination
│
├─── lucidia (Pi 5 8GB, .81) ─────────── AI INFERENCE [offline]
│    │   Tailscale: 100.83.149.86
│    │   Services: ollama, agent-orchestration
│    │   Agent capacity: 7,500
│    └── pironman     case  SunFounder Pironman 5  [online]
│        │                  Active cooling (ICE Tower)
│        │                  OLED status display
│        │                  RGB LED fan
│        │                  Safe shutdown button
│        │                  Built-in M.2 NVMe slot
│        └── lucidia-nvme  M.2  1TB NVMe SSD  [offline]
│                               Mounted through Pironman's M.2 slot
│
├─── aria (Pi 5, .82) ────────────────── DATA SCIENCE [offline]
│        Tailscale: 100.109.14.17
│        Services: ml-pipelines, data-analysis
│
├─── pandora (65" Roku TV, .26) ──────── LIVING ROOM
│    └── calliope     HDMI  Roku Streaming Stick Plus 3830R  [online]
│                           Has own network IP: .33
│                           API: http://192.168.4.33:8060
│
├─── athena (.27)  iPhone/iPad ────────── AirPlay + lockdownd
├─── phantom (.88) Phone (randomized MAC)
├─── specter (.92) Phone (randomized MAC)
├─── ember (.22)   AltoBeam IoT device
├─── wraith (.44)  Silent, no ports
├─── vesper (.45)  Silent, no ports
└─── cortana (.90) Xbox/Surface [sleeping]


CLOUD (DigitalOcean, not on LAN)
├── anastasia (174.138.44.45) ─── EDGE COMPUTE
│       Tailscale: 100.94.33.37
│       Services: edge-compute, agent-runtime
└── gematria  (159.65.43.12) ──── CLOUD ORACLE
        Tailscale: 100.108.132.8
        Services: websocket, api, mining
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
              ┌──────────┬─────────┬───────────────┼─────────────┬──────────┐
              │          │         │               │             │          │
       ┌──────▼──┐ ┌─────▼───┐ ┌──▼─────┐  ┌─────▼────┐ ┌─────▼───┐ ┌────▼───┐
       │alexandria│ │ cecilia │ │octavia │  │  alice   │ │ lucidia │ │  aria  │
       │ Mac M1  │ │  Pi 5   │ │  Pi 5  │  │  Pi 4   │ │  Pi 5   │ │  Pi 5  │
       └────┬────┘ └────┬────┘ └────────┘  └─────────┘ └────┬────┘ └────────┘
            │            │                                    │
     ┌──────┼──────┐  ┌──┴──────┐                    ┌───────┴───────┐
     │      │      │  │         │                    │               │
  [siren][lyra][wave] [hailo8] [nvme]            [pironman]         │
   USB    USB   USB   PCIe     USB              case+cooler     [nvme]
                      26 TOPS  500GB            OLED+RGB        1TB M.2
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
  .27  athena       Mobile (iPhone/iPad)
  .28  alexandria   Workstation (Mac M1) ← siren, lyra, wavecube via USB
  .33  calliope     Streaming (Roku Stick, physically on pandora)
  .38  octavia      Pi 5 (compute)
  .44  wraith       Unknown (silent)
  .45  vesper       Unknown (silent)
  .49  alice        Pi 4 (worker)
  .81  lucidia      Pi 5 (inference) ← pironman case → 1TB NVMe
  .82  aria         Pi 5 (data science)
  .88  phantom      Mobile (privacy MAC)
  .89  cecilia      Pi 5 (CECE OS) ← Hailo-8 + 500GB NVMe
  .90  cortana      Console (Xbox/Surface)
  .92  specter      Mobile (privacy MAC)
```

## Device Count

```
  Compute hosts (6)  ██████████████████████  alexandria, cecilia, octavia, alice, lucidia, aria
  Sub-devices (8)    ████████████████████████████  hailo8, nvme x2, pironman, siren, lyra, wavecube, calliope
  Cloud (2)          ██████                        anastasia, gematria
  Media (2)          ██████                        pandora, cortana
  Mobile (3)         █████████                     athena, phantom, specter
  IoT (1)            ███                           ember
  Unknown (2)        ██████                        wraith, vesper
  Router (1)         ███                           meridian
```
