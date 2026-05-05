<div align="center">

```
██╗      ██████╗  █████╗ ██████╗ ███████╗████████╗██████╗ ██╗██╗  ██╗███████╗
██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██║██║ ██╔╝██╔════╝
██║     ██║   ██║███████║██║  ██║███████╗   ██║   ██████╔╝██║█████╔╝ █████╗  
██║     ██║   ██║██╔══██║██║  ██║╚════██║   ██║   ██╔══██╗██║██╔═██╗ ██╔══╝  
███████╗╚██████╔╝██║  ██║██████╔╝███████║   ██║   ██║  ██║██║██║  ██╗███████╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚══════╝
```

# ⚡ LoadStrike Pro — v11.0

### Self-Learning L4/L7 Load Testing Framework with AI Brain Engine

<br>

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-Proprietary-FF4444?style=for-the-badge&logo=opensourceinitiative&logoColor=white)
![Version](https://img.shields.io/badge/Version-11.0-00C896?style=for-the-badge&logo=semver&logoColor=white)
![Async](https://img.shields.io/badge/Async-aiohttp%20%2B%20uvloop-FF6B35?style=for-the-badge&logo=asyncapi&logoColor=white)
![HTTP2](https://img.shields.io/badge/HTTP%2F2-Supported-6C5CE7?style=for-the-badge&logo=cloudflare&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-Ready-27AE60?style=for-the-badge&logo=githubactions&logoColor=white)

<br>

> **LoadStrike Pro** is a next-generation, self-learning performance testing engine.
> It combines an AI-powered Brain Engine, 21+ attack modes, HAR session replay,
> and real-time dashboards into a single professional-grade CLI tool.

</div>

---

## ⚠️ LEGAL WARNING — READ BEFORE USE

> ```
> ╔══════════════════════════════════════════════════════════════════════════════╗
> ║                     ⛔  AUTHORIZED USE ONLY  ⛔                             ║
> ║                                                                              ║
> ║  LoadStrike Pro is a professional security and performance testing tool.     ║
> ║  Use of this tool against systems, networks, or services that you do NOT     ║
> ║  own, or do NOT have EXPLICIT WRITTEN PERMISSION to test, is:                ║
> ║                                                                              ║
> ║    • ILLEGAL under the Computer Fraud and Abuse Act (CFAA)                  ║
> ║    • ILLEGAL under the Computer Misuse Act (CMA) and equivalents            ║
> ║    • Subject to CRIMINAL PROSECUTION and CIVIL LIABILITY                    ║
> ║                                                                              ║
> ║  The author(s) of this tool accept ZERO responsibility for any misuse,      ║
> ║  damage, data loss, service disruption, or legal consequences arising        ║
> ║  from unauthorized deployment of this software.                             ║
> ║                                                                              ║
> ║  ✅ PERMITTED:  Your own servers / infrastructure you own                   ║
> ║  ✅ PERMITTED:  Environments with signed written authorization               ║
> ║  ✅ PERMITTED:  Sandboxed / isolated lab environments                        ║
> ║  ❌ FORBIDDEN:  Any third-party system without explicit written consent      ║
> ║  ❌ FORBIDDEN:  Public websites, APIs, or cloud services you don't own       ║
> ║  ❌ FORBIDDEN:  Government, military, or critical infrastructure             ║
> ╚══════════════════════════════════════════════════════════════════════════════╝
> ```

---

## 🔒 INTELLECTUAL PROPERTY — REVERSE ENGINEERING PROHIBITED

> ```
> ╔══════════════════════════════════════════════════════════════════════════════╗
> ║               🚫  REVERSE ENGINEERING STRICTLY FORBIDDEN  🚫                ║
> ║                                                                              ║
> ║  This software and its source code are protected intellectual property.      ║
> ║  The following actions are STRICTLY PROHIBITED without prior written         ║
> ║  authorization from the copyright holder:                                   ║
> ║                                                                              ║
> ║    ✗  Decompiling, disassembling, or reverse engineering any component      ║
> ║    ✗  Extracting, copying, or redistributing source code                    ║
> ║    ✗  Creating derivative works or forks without permission                 ║
> ║    ✗  Using the codebase to build competing products                        ║
> ║    ✗  Removing or altering copyright notices or license headers             ║
> ║                                                                              ║
> ║  Violation constitutes copyright infringement and will be prosecuted        ║
> ║  to the fullest extent of applicable intellectual property law.             ║
> ╚══════════════════════════════════════════════════════════════════════════════╝
> ```

---

## 📋 Table of Contents

| # | Section |
|---|---------|
| 1 | [⚡ Quick Start](#-quick-start) |
| 2 | [🧠 How It Works — Architecture](#-how-it-works--architecture) |
| 3 | [🤖 Brain Engine (AI Self-Learning)](#-brain-engine--ai-self-learning) |
| 4 | [🌐 L7 Modes — Application Layer](#-l7-modes--application-layer) |
| 5 | [🔌 L4 Modes — Transport Layer](#-l4-modes--transport-layer) |
| 6 | [🎬 HAR Playback — Session Replay](#-har-playback--session-replay) |
| 7 | [📜 Scenario 2.0 Engine](#-scenario-20-engine) |
| 8 | [📊 Live Dashboard & Reporting](#-live-dashboard--reporting) |
| 9 | [🔗 Integrations & Alerts](#-integrations--alerts) |
| 10 | [⚙️ All CLI Options](#️-all-cli-options) |
| 11 | [📦 Installation & Requirements](#-installation--requirements) |
| 12 | [🔄 CI/CD Pipeline Integration](#-cicd-pipeline-integration) |
| 13 | [🧩 Plugin System](#-plugin-system) |

---

## ⚡ Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Basic load test — 100 concurrent workers, 30 seconds
python loadstrike.py https://example.com -c 100 -d 30

# 3. Specific mode — keep-alive connections, 200 workers, 60 seconds
python loadstrike.py https://example.com -m keepalive -c 200 -d 60

# 4. Auto-generate full report
python loadstrike.py https://example.com -c 100 -d 30 --report

# 5. Run with Brain Engine (AI auto-tuning)
python loadstrike.py https://example.com -c 100 -d 60 --brain-show example.com
```

---

## 🧠 How It Works — Architecture

LoadStrike Pro is built on a layered, async-first architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                       loadstrike.py                             │
│                     [ Entry Point / CLI ]                       │
└─────────────────────────────┬───────────────────────────────────┘
                              │
          ┌───────────────────▼───────────────────┐
          │           core/runner.py               │
          │     [ Async Orchestrator Engine ]       │
          │   Routes: L4 / L7 / HAR / Scenario     │
          └──┬──────────────┬──────────────┬───────┘
             │              │              │
    ┌────────▼───┐  ┌───────▼──────┐ ┌────▼──────────┐
    │  L7 Modes  │  │  L4 Modes    │ │  HAR Playback  │
    │ (21 modes) │  │ (5 modes)    │ │  Session Replay│
    └────────────┘  └──────────────┘ └────────────────┘
             │              │              │
          ┌──▼──────────────▼──────────────▼───┐
          │            core/brain.py            │
          │    [ UCB1 Self-Learning Engine ]     │
          │  Learns optimal concurrency per host │
          └──────────────┬──────────────────────┘
                         │
          ┌──────────────▼──────────────────────┐
          │           core/stats.py              │
          │  [ Thread-Safe Stats Engine ]        │
          │  O(log n) Percentiles: P50/P95/P99  │
          └──────────────┬──────────────────────┘
                         │
     ┌───────────────────▼─────────────────────────┐
     │          Output / Reporting Layer            │
     │  Dashboard │ HTML Report │ JSON │ JUnit XML  │
     │  Prometheus │ Slack │ PagerDuty │ CSV        │
     └─────────────────────────────────────────────┘
```

**Request Lifecycle:**

```
User CLI Input
     │
     ▼
Config Loader (YAML/TOML/JSON + .env secrets)
     │
     ▼
Brain Engine → suggests optimal concurrency
     │
     ▼
Token Bucket Rate Limiter → controls RPS ceiling
     │
     ▼
Multi-Process Engine (optional) → breaks Python GIL
     │
     ▼
Async Worker Pool → fires concurrent requests
     │
     ▼
Stats Engine → collects latencies, errors, RPS
     │
     ▼
Live Dashboard (terminal) + WebSocket feed
     │
     ▼
Reports + Alerts (HTML, JSON, JUnit, Slack, PD)
```

---

## 🤖 Brain Engine — AI Self-Learning

The Brain Engine uses the **UCB1 Multi-Armed Bandit algorithm** to learn the optimal configuration for each target host over time.

```
┌─────────────────────────────────────────────────────┐
│                  Brain Engine (UCB1)                │
│                                                     │
│  • Tracks 5 concurrency arms per host               │
│  • Scores: RPS × (1 - error_rate)                   │
│  • Exploration bonus: c × √(ln(N) / tries)          │
│  • Time-bucketed: learns per weekday+hour           │
│  • Anomaly detection: baseline P95 + RPS deltas     │
│  • Regression history: compares runs over time      │
└─────────────────────────────────────────────────────┘
```

```bash
# View the learned profile for a host
python loadstrike.py --brain-show example.com

# Reset the profile for a specific host
python loadstrike.py --brain-reset example.com

# Reset ALL learned profiles
python loadstrike.py --brain-reset-all

# Use a custom Brain database file
python loadstrike.py https://example.com --brain-file /path/to/custom.json
```

**What the Brain stores per host:**
- ✅ Optimal concurrency & burst size
- ✅ Keep-alive & pipeline support flags
- ✅ Average response time & max stable RPS
- ✅ Time-of-day performance profiles
- ✅ Anomaly baselines (P95, RPS)
- ✅ Full regression history across runs

---

## 🌐 L7 Modes — Application Layer

> All L7 modes operate at the HTTP/WebSocket/gRPC application layer.

| Mode | Icon | Description |
|------|------|-------------|
| `http` | 🌊 | Standard HTTP flood with randomized headers & User-Agents |
| `keepalive` | 🔗 | Keep-alive connection reuse — most realistic traffic pattern |
| `slowloris` | 🐌 | Hold connections open with incomplete headers |
| `rudy` | 💧 | Slow POST body — R-U-Dead-Yet attack pattern |
| `slow_read` | 🐢 | Read responses byte-by-byte to exhaust server buffers |
| `cache_bypass` | 🚫 | Unique query strings to bypass CDN / edge caches |
| `range` | 🔢 | Byte-range fragmentation requests |
| `tls` | 🔐 | Repeated TLS handshake exhaustion |
| `h2_reset` | ⚡ | HTTP/2 Rapid Reset (CVE-2023-44487) |
| `header_overflow` | 📨 | 100–250 large headers per request |
| `connection` | 📡 | TCP connection flood at L7 |
| `dns` | 🔍 | DNS resolver stress testing |
| `payload` | 📦 | Large POST body flood |
| `scenario` | 📋 | Multi-step flows with variable extraction |
| `chaos` | 🎲 | Random error/latency injection for resilience testing |
| `mixed` | 🧩 | Brain-adaptive mix cycling all available modes |
| `grpc` | ⚙️ | gRPC unary flood |
| `websocket` | 🔄 | WebSocket message flood |
| `graphql` | 📊 | GraphQL query flood |
| `h2_multiplex` | 🚀 | True HTTP/2 stream multiplexing via httpx |
| `har` | 🎬 | **HAR file playback — real browser session replay** |

```bash
# Examples
python loadstrike.py https://example.com -m keepalive   -c 200 -d 60
python loadstrike.py https://example.com -m slowloris   -c 150 -d 120
python loadstrike.py https://example.com -m h2_reset    -c 100 -d 30
python loadstrike.py https://example.com -m websocket   -c 50  -d 60
python loadstrike.py https://example.com -m graphql     -c 80  -d 45
python loadstrike.py https://example.com -m mixed       -c 300 -d 120
```

---

## 🔌 L4 Modes — Transport Layer

> ⚠️ **L4 modes operate at the network transport layer. Use ONLY on systems you own or have explicit written authorization to test.**

| Mode | Icon | Description | Root Required |
|------|------|-------------|:---:|
| `tcp_flood` | 🌊 | High-volume TCP connection flood | ❌ No |
| `udp_flood` | 💥 | UDP packet flood | ❌ No |
| `syn_flood` | ⚡ | TCP SYN flood with raw sockets | ✅ **Yes** |
| `connection_flood_l4` | 🔗 | Sustained open TCP connections | ❌ No |
| `udp_amplify` | 📡 | UDP amplification probe (DNS/NTP) | ❌ No |

```bash
# TCP flood — 500 workers, 30 seconds
python loadstrike.py https://myserver.com -m tcp_flood -c 500 -d 30

# UDP flood — custom port, 200 workers
python loadstrike.py https://myserver.com -m udp_flood --l4-port 80 -c 200 -d 30

# SYN flood — requires root/sudo
sudo python loadstrike.py https://myserver.com -m syn_flood --l4-port 443 -c 100 -d 30

# UDP amplification probe
python loadstrike.py https://myserver.com -m udp_amplify --l4-port 53 -c 50 -d 30
```

---

## 🎬 HAR Playback — Session Replay

Record a real browser session and replay it at scale as a load test.

```
Browser Session Recording
        │
        ▼
  Chrome DevTools
  Network → Export HAR
        │
        ▼
  session.har file
        │
        ▼
  LoadStrike HAR Replay Engine
  ┌─────────────────────────────┐
  │  • Extracts all requests    │
  │  • Preserves timing/order   │
  │  • Filters by URL pattern   │
  │  • Controls replay speed    │
  │  • Scales to N workers      │
  └─────────────────────────────┘
        │
        ▼
  Realistic Multi-User Load Test
```

```bash
# In Chrome: DevTools (F12) → Network tab → Export HAR

# Basic HAR replay — 50 workers, 60 seconds
python loadstrike.py https://mysite.com -m har --har-file session.har -c 50 -d 60

# 2x faster playback, filter only /api/ routes
python loadstrike.py https://mysite.com -m har --har-file session.har --har-speed 2.0 --har-filter /api/
```

---

## 📜 Scenario 2.0 Engine

Build complex multi-step test flows with variable extraction, conditionals, and parallel steps.

```yaml
# scenario.yaml
scenario:
  # Step 1 — Login and extract token
  - url: /api/login
    method: POST
    body: '{"user":"test","pass":"test"}'
    extract:
      token: access_token      # JSON path extraction
    assert_status: 200
    on_fail: abort             # abort | continue | retry

  # Step 2 — Authenticated request using extracted token
  - url: /api/data
    method: GET
    headers:
      Authorization: "Bearer {{token}}"
    condition: "token != ''"   # skip step if condition is falsy

    # Step 3 — Run these steps in parallel
    parallel:
      - url: /api/metrics
      - url: /api/health
```

```bash
# Run scenario test
python loadstrike.py https://mysite.com -m scenario --config scenario.yaml -c 100 -d 60
```

**Scenario Features:**
- ✅ JSON path variable extraction
- ✅ Template variable injection `{{token}}`
- ✅ Conditional step execution
- ✅ Parallel step groups
- ✅ Per-step failure strategy: `abort | continue | retry`
- ✅ Status code assertions

---

## 📊 Live Dashboard & Reporting

### Live Terminal Dashboard

```
╔══════════════════════════════════════════════════════════════╗
║  LoadStrike Pro v11  │  Target: example.com  │  00:00:42    ║
╠══════════════════════════════════════════════════════════════╣
║  RPS: 4,823   │  Total: 201,850   │  Errors: 0.2%          ║
║  P50: 18ms    │  P95: 87ms        │  P99: 234ms            ║
║  Workers: 200 │  Active: 198      │  Mode: keepalive       ║
╠══════════════════════════════════════════════════════════════╣
║  Brain: optimal concurrency=200  anomaly=none              ║
╚══════════════════════════════════════════════════════════════╝
```

### Report Formats

| Format | Flag | Contents |
|--------|------|----------|
| 📊 HTML | `--report` | Interactive Chart.js dashboard with full timeline |
| 📄 JSON | `--output-json` | Machine-readable full stats dump |
| 🧪 JUnit XML | `--output-junit results.xml` | CI/CD test results format |
| 📈 CSV | `--output-csv timeseries.csv` | Time-series RPS/latency data |
| 🔥 Prometheus | `--prometheus-port 9090` | Live metrics scraping endpoint |
| 🌐 WebSocket | `--live-port 8080` | Real-time live feed for custom dashboards |

```bash
# Generate all report formats
python loadstrike.py https://example.com -c 200 -d 60 \
  --report \
  --output-junit results.xml \
  --output-csv timeseries.csv
```

---

## 🔗 Integrations & Alerts

### Supported Alert Channels

| Integration | Trigger |
|-------------|---------|
| 💬 **Slack** | Test start/end, threshold breach, anomaly detected |
| 📟 **PagerDuty** | Critical failures, SLA breach |
| 🌐 **Custom Webhook** | Any event → POST JSON payload |
| 📊 **Prometheus** | Live metric scraping at `/metrics` |

### Environment Variables (Secrets)

```bash
# .env file — never commit secrets to version control
LOADSTRIKE_SLACK_WEBHOOK=https://hooks.slack.com/services/...
LOADSTRIKE_PD_KEY=your-pagerduty-integration-key
LOADSTRIKE_AUTH_TOKEN=Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6...
```

```yaml
# config.yaml — reference env vars with $ prefix
auth:
  token: $LOADSTRIKE_AUTH_TOKEN

alerts:
  slack_webhook: $LOADSTRIKE_SLACK_WEBHOOK
  pagerduty_key: $LOADSTRIKE_PD_KEY
```

```bash
# Load secrets from .env automatically
python loadstrike.py https://example.com --config config.yaml --env-file .env
```

---

## ⚙️ All CLI Options

```
┌─────────────────────────────────────────────────────────────────────┐
│                    CORE OPTIONS                                     │
├─────────────────┬───────────────────────────────────────────────────┤
│ -m, --mode      │ Test mode (see L7/L4 tables above)                │
│ -c, --concurrency│ Number of concurrent workers (default: 100)      │
│ -d, --duration  │ Test duration in seconds (default: 30)            │
│ --rampup        │ Ramp-up duration in seconds                       │
│ --warmup        │ Warm-up duration in seconds                       │
│ --rate-limit    │ Max requests per second (token bucket)            │
├─────────────────┴───────────────────────────────────────────────────┤
│                    BRAIN ENGINE                                     │
├─────────────────┬───────────────────────────────────────────────────┤
│ --brain-show    │ View learned profile for a host                   │
│ --brain-reset   │ Reset profile for a specific host                 │
│ --brain-reset-all│ Reset ALL learned profiles                       │
│ --brain-file    │ Custom Brain database file path                   │
├─────────────────┴───────────────────────────────────────────────────┤
│                    L4 OPTIONS                                       │
├─────────────────┬───────────────────────────────────────────────────┤
│ --l4-port       │ Target port for L4 modes                          │
│ --l4-pps        │ Packets per second limit for L4                   │
├─────────────────┴───────────────────────────────────────────────────┤
│                    HAR PLAYBACK                                     │
├─────────────────┬───────────────────────────────────────────────────┤
│ --har-file      │ Path to the HAR file for replay mode              │
│ --har-speed     │ Replay speed multiplier (e.g. 2.0 = 2x faster)   │
│ --har-filter    │ Filter requests by URL pattern                    │
├─────────────────┴───────────────────────────────────────────────────┤
│                    CONFIGURATION                                    │
├─────────────────┬───────────────────────────────────────────────────┤
│ --config        │ YAML / TOML / JSON config file                    │
│ --env-file      │ .env file for secrets (default: .env)             │
├─────────────────┴───────────────────────────────────────────────────┤
│                    PERFORMANCE                                      │
├─────────────────┬───────────────────────────────────────────────────┤
│ --multiprocess  │ One process per CPU core (breaks Python GIL)      │
│ --distributed   │ Run distributed across multiple nodes             │
├─────────────────┴───────────────────────────────────────────────────┤
│                    OUTPUT & REPORTING                               │
├─────────────────┬───────────────────────────────────────────────────┤
│ --report        │ Auto-generate HTML + JSON + JUnit reports         │
│ --output-junit  │ JUnit XML output file path                        │
│ --output-csv    │ CSV time-series output file path                  │
│ --live-port     │ WebSocket port for live dashboard                 │
│ --prometheus-port│ Prometheus metrics scraping port                 │
├─────────────────┴───────────────────────────────────────────────────┤
│                    CI/CD THRESHOLDS                                 │
├─────────────────┬───────────────────────────────────────────────────┤
│ --max-error-rate│ Max acceptable error rate % (exit 1 on breach)    │
│ --max-p95       │ Max acceptable P95 latency in ms (exit 1 on breach)│
│ --ci            │ CI mode — silent output + strict exit codes        │
└─────────────────┴───────────────────────────────────────────────────┘
```

---

## 📦 Installation & Requirements

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| 🐍 Python | 3.10+ | 3.12+ |
| 💾 RAM | 256 MB | 1 GB+ |
| 🖥️ OS | Linux / macOS | Linux (for uvloop boost) |
| 🔑 Root/sudo | Not required | Required for `syn_flood` only |

### Installation

```bash
# Clone or extract the archive
cd ls_v11/

# Install core dependencies only
pip install aiohttp>=3.9.0

# Install all dependencies (recommended)
pip install -r requirements.txt

# Verify installation
python loadstrike.py --help
```

### Dependencies Breakdown

```
REQUIRED ──────────────────────────────────────────────────────
  aiohttp>=3.9.0           Async HTTP + WebSocket engine (core)

PERFORMANCE ────────────────────────────────────────────────────
  uvloop>=0.19.0           libuv event loop — 30–80% RPS boost (Linux/macOS)
  sortedcontainers>=2.4.0  O(log n) percentile calculation

CONFIGURATION ──────────────────────────────────────────────────
  pyyaml>=6.0              YAML config file support
  tomli>=2.0.0             TOML config support (Python < 3.11)
  aiohttp-socks>=0.8.0     SOCKS5 proxy support

HTTP/2 & gRPC ──────────────────────────────────────────────────
  httpx[http2]>=0.27.0     HTTP/2 stream multiplexing
  grpcio>=1.60.0           gRPC flood mode
  grpcio-tools>=1.60.0     gRPC proto compilation (optional)

DASHBOARD & DISTRIBUTED ────────────────────────────────────────
  websockets>=12.0         Live dashboard + distributed mode

REPORTING ──────────────────────────────────────────────────────
  weasyprint>=60.0         PDF report export

TESTING ────────────────────────────────────────────────────────
  pytest>=8.0.0            Test runner
  pytest-asyncio>=0.23.0   Async test support
```

---

## 🔄 CI/CD Pipeline Integration

LoadStrike Pro integrates natively into CI/CD pipelines with threshold-based exit codes.

```bash
# CI pipeline command — fails build if thresholds are breached
python loadstrike.py https://staging.mysite.com \
  -c 200 \
  -d 60 \
  --max-error-rate 5 \
  --max-p95 1000 \
  --output-junit results.xml \
  --output-csv timeseries.csv \
  --ci
```

```
Exit Code 0 ✅  →  All thresholds passed
Exit Code 1 ❌  →  Threshold breach detected
```

### GitHub Actions Example

```yaml
# .github/workflows/load-test.yml
- name: Run Load Test
  run: |
    pip install -r requirements.txt
    python loadstrike.py ${{ secrets.STAGING_URL }} \
      -c 200 -d 60 \
      --max-error-rate 5 --max-p95 1000 \
      --output-junit load-test-results.xml --ci

- name: Publish Results
  uses: actions/upload-artifact@v3
  with:
    name: load-test-results
    path: load-test-results.xml
```

---

## 🧩 Plugin System

Extend LoadStrike Pro with custom plugins.

```python
# plugins/my_plugin.py
from plugins import BasePlugin

class MyPlugin(BasePlugin):
    name = "my_plugin"

    async def on_request_start(self, context):
        # Hook: before each request
        pass

    async def on_request_end(self, context, response):
        # Hook: after each request
        pass

    async def on_test_complete(self, stats):
        # Hook: when the full test finishes
        pass
```

```bash
# Plugin is auto-discovered from the plugins/ directory
python loadstrike.py https://example.com --plugin my_plugin
```

---

## 📁 Project Structure

```
ls_v11/
├── loadstrike.py              ← Entry point
│
├── core/
│   ├── cli.py                 ← Argument parsing, output, reporting
│   ├── runner.py              ← Async orchestrator (L4/L7/HAR routing)
│   ├── brain.py               ← Self-learning UCB1 engine
│   ├── stats.py               ← Thread-safe stats + O(log n) percentiles
│   ├── config.py              ← Config dataclasses (YAML/TOML/JSON)
│   ├── dashboard.py           ← Live terminal dashboard
│   ├── token_bucket.py        ← Precise RPS rate limiter
│   └── mp_engine.py           ← Multi-process engine (GIL bypass)
│
├── modes/
│   ├── runners.py             ← All 21 L7 worker coroutines
│   ├── h2_multiplex.py        ← HTTP/2 multiplexing via httpx
│   └── har_playback.py        ← HAR file replay engine
│
├── l4/
│   └── modes.py               ← L4 workers: TCP/UDP/SYN flood
│
├── plugins/
│   ├── __init__.py            ← Plugin base class + auto-loader
│   └── example_plugin.py      ← Example plugin implementations
│
├── integrations/
│   └── alerts.py              ← Slack, PagerDuty, Webhook, Prometheus
│
├── reporting/
│   ├── html_report.py         ← Interactive Chart.js HTML report
│   └── baseline.py            ← Baseline comparison + CI exit codes
│
├── tests/
│   └── test_core.py           ← Full pytest suite (60+ tests)
│
└── requirements.txt
```

---

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run the full test suite (60+ tests)
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=core --cov=modes --cov=l4
```

---

<div align="center">

---

**LoadStrike Pro v11.0** — Built for engineers who test what they own.

*Use responsibly. Test ethically. Protect your systems.*

---

</div>
