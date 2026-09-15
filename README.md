# 🚀 Nexora — Operational Risk & Supply Intelligence Platform

> **IBM Bob AI Innovation Hackathon 2026**  
> **Track:** AI  
> **Problem Statement S2:** Fab Bottleneck & Supply Chain Risk Advisor

---

## 👥 Team & Repository

| Field | Value |
|---|---|
| **Project** | **Nexora — Operational Risk & Supply Intelligence Platform** |
| **Team Name** | **Stack_Trace** |
| **Track** | Semiconductor |
| **Repository** | [https://github.com/neel92654/bob-ai-hackathon-Stack_Trace](https://github.com/neel92654/bob-ai-hackathon-Stack_Trace) |
| **Team Lead** | Neel Patel — `neel92654@gmail.com` |
| **Members** | Mayank Padmani, Meet Ramani, Kremil Dobariya |

---

## 🎯 Problem Statement

Chip lead times are 26–52 weeks. Bottlenecks at specific process steps (lithography, etch, CVD) cause cascading delivery delays — the 2021 chip shortage halted auto
factories for months. Simultaneously, single-source suppliers for critical materials (gallium, neon, photoresists) create catastrophic risk: China controls 80%+ of gallium
and germanium, both now under export controls.

---

## 💡 Solution

**Nexora** is an explainable operational intelligence platform designed for semiconductor fab operators and supply chain planners. It continuously analyzes equipment WIP queue pressures across sequential manufacturing stages, predicts order delivery delays using a trained `RandomForestRegressor` ML model ($R^2 = 0.954$), evaluates single-point-of-failure (SPoF) suppliers and geopolitical concentration risks, simulates multi-day operational disruptions through an interactive What-If engine, and synthesizes prioritized, condition-driven mitigation protocols.

---

## 🤖 IBM Bob Integration (Model Context Protocol)

Nexora integrates with **IBM Bob** using the **Model Context Protocol (MCP)**. In this architecture:
1. **IBM Bob acts as the AI Agent / Interface:** The user asks natural-language operational questions directly to Bob.
2. **Nexora MCP Server (`mcp-server/`):** Exposes 8 structured operational intelligence tools to Bob over standard STDIO transport.
3. **Tool Discovery & Execution:** Bob automatically discovers Nexora's tools via `.bob/mcp.json` and invokes the appropriate tool when answering questions.
4. **Verified Telemetry & Grounding:** Nexora executes the underlying analytics/ML calculation and returns structured data.
5. **Explainable Decision Support:** Bob uses the verified operational data to explain the root causes, quantify delivery impacts, and provide prescriptive guidance.

### Architecture Diagram
```
IBM Bob (MCP Client / Agent)
      │
      ▼ (STDIO Transport / JSON-RPC via .bob/mcp.json)
Nexora MCP Server (mcp-server/server.py)
      │
      ▼ (Reuses existing analytics services — zero logic duplication)
Nexora Analytics, ML & Simulation Engines
      │
      ▼
SQLite Database (nexora.db) + ML Model (delivery_model.joblib)
      │
      ▼
Verified Operational Fab & Supply Telemetry
```

### Registered MCP Tools for IBM Bob
- `get_fab_bottlenecks`: Fab equipment queue overloads, utilization %, severity, and affected lot counts.
- `get_bottleneck_details`: Deep-dive root-cause diagnostics, chamber health, MTBF, and assigned wafer lots for a specific tool ID (`CVD-03`, `LITH-01`).
- `get_supplier_risk`: Explainable 5-factor supplier risk ranking (0–100), SPoF flags, and geopolitical exposures.
- `get_supplier_details`: Complete risk profiling, factor breakdowns, and alternate source availability for a supplier ID (`SUP-002`).
- `get_production_impact`: Active wafer lot tracking across 10 manufacturing stages with ML delivery delay predictions.
- `run_disruption_simulation`: Executes What-If disruption simulations (Supplier Disruption, Tool Breakdown, Capacity Derating, Demand Surge) with Before vs. After metric diffs and SLA financial exposure.
- `get_recommendations`: Prioritized, condition-driven mitigation action plans with operational rationales and expected benefits.
- `get_executive_summary`: High-level executive operational summary of fab risk score, critical alerts, and top mitigations.

---

## ✨ Key Features

- **Fab Bottleneck Intelligence:** Real-time tool utilization tracking ($\text{Utilization} = \text{WIP} / \text{Capacity} \times 100$), queue pressure metrics, and 10-stage downstream process flow starvation mapping.
- **Explainable 5-Factor Supplier Risk Scoring:** Transparent 0–100 risk scoring with automated Single-Point-of-Failure (SPoF) detection and country-level geopolitical concentration analytics.
- **Interpretable ML Delivery Delay Prediction:** Validated scikit-learn regression model ($R^2 = 0.954$, MAE = 2.81h) attributing feature contributions with an automatic deterministic physics fallback.
- **Interactive 4-Scenario What-If Disruption Simulator:** Simulates supplier embargoes, equipment outages, capacity derating, and demand surges with Before vs. After metric diffs and financial SLA exposure calculations.
- **Condition-Driven Recommendation Engine:** Prescriptive mitigation protocols dynamically generated from active queue overloads, chamber health drifts, and single-source dependencies.
- **Real MCP Server for IBM Bob:** 8 native tools exposing full fab analytics, simulations, and recommendations to IBM Bob.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Languages** | Python 3.11, JavaScript (ES6+), SQL, HTML5, CSS3 |
| **Backend & ML** | Flask, Flask-CORS, scikit-learn, Pandas, NumPy, Joblib |
| **MCP & Agent Layer** | Model Context Protocol (MCP SDK 2.x), `.bob/mcp.json` |
| **Frontend** | React 18, Vite, Lucide Icons, Custom Modern CSS Design System |
| **IBM Technologies** | IBM Bob + MCP Integration |
| **Databases** | SQLite (`nexora.db`) |
| **Testing & CI** | Pytest (52 automated tests passing), GitHub Actions |

---

## 📁 Repository Structure

```
├── .bob/                      # IBM Bob MCP client configuration
│   └── mcp.json               # STDIO transport configuration for IBM Bob
├── mcp-server/                # Model Context Protocol (MCP) Server for IBM Bob
│   ├── server.py              # 8 MCP tools adapter connecting to Nexora services
│   ├── requirements.txt       # MCP server dependencies
│   └── README.md              # MCP server documentation
├── src/
│   ├── backend/               # Flask REST API, calculations, routes, services & ML
│   │   ├── app.py             # Flask application gateway
│   │   ├── config/            # Configurable risk thresholds & weights
│   │   ├── models/            # SQLite connection and schema
│   │   ├── routes/            # REST API blueprints (7 endpoints)
│   │   ├── services/          # Core analytics & decision engines
│   │   ├── ml/                # RandomForestRegressor pipeline & inference
│   │   └── utils/             # Pure calculation & validation functions
│   ├── frontend/              # React 18 + Vite industrial dashboard UI
│   │   ├── src/components/    # Modular UI components (Navbar, Flow, Badges, Modals)
│   │   ├── src/pages/         # 7 core views (Dashboard, Bottlenecks, Supply, Simulator...)
│   │   └── src/services/      # Centralized REST API client
│   ├── data/                  # Synthetic CSV datasets (equipment, lots, suppliers...)
│   ├── .env.example           # Environment variable template
│   └── README.md              # Source code directory overview
├── docs/                      # Comprehensive documentation
│   ├── problem-statement.md   # Domain context & pain points
│   ├── solution-overview.md   # Architecture, workflows & design choices
│   ├── architecture.md        # Technical architecture with Mermaid diagrams
│   ├── setup-guide.md         # Step-by-step reproduction instructions
│   └── template-guide.md      # Template guide
├── demo/                      # Demo artifacts
│   ├── screenshots/           # 5 application screenshots
│   ├── demo-video-link.txt    # Video walkthrough link
│   └── live-demo-url.txt      # Local/hosted deployment details
├── presentation/              # Slide deck documentation
│   ├── README.md
│   └── slides.md
├── scripts/                   # Reproducible generator & database initializers
│   ├── generate_data.py       # Deterministic synthetic data generator (Seed: 42)
│   └── init_db.py             # SQLite ingestion script
├── tests/                     # 52 automated backend & MCP tests
├── submission.yaml            # Structured submission metadata
├── CONTRIBUTING.md            # Submission instructions
└── README.md                  # Main project entry point
```

---

## ⚡ How to Run

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ and npm 9+

### 2. Backend & Data Setup
```bash
# Generate synthetic dataset (Seed: 42)
python3 scripts/generate_data.py

# Initialize SQLite database
python3 scripts/init_db.py

# Train the ML Delivery Prediction model
python3 src/backend/ml/train_delivery_model.py

# Run full automated test suite (52 tests including MCP)
pytest tests/ -v

# Start Flask backend API (Port 5001)
python3 src/backend/app.py
```

### 3. Connect IBM Bob to Nexora MCP Server
IBM Bob automatically connects to Nexora using `.bob/mcp.json`. To run or test the MCP server manually:
```bash
python3 mcp-server/server.py
```

### 4. Frontend Setup (In a separate terminal)
```bash
cd src/frontend
npm install
npm run dev
```
Open your browser at `http://localhost:5173`.

---

## 🖥️ Demo & Screenshots

| Artifact | Link |
|---|---|
| 📹 Demo Video | [See demo/demo-video-link.txt](demo/demo-video-link.txt) |
| 🌐 Live Demo | [See demo/live-demo-url.txt](https://nexora-7cs9.onrender.com/) |
| 🖼️ Executive Dashboard | ![Dashboard](demo/screenshots/01-dashboard.png) |
| 🖼️ Bottleneck Intelligence | ![Bottlenecks](demo/screenshots/02-bottleneck-analysis.png) |
| 🖼️ Supply Chain SPoF & Geopolitical | ![Supply Chain](demo/screenshots/03-supplier-risk.png) |
| 🖼️ What-If Disruption Simulator | ![Simulator](demo/screenshots/04-what-if-simulation.png) |
| 🖼️ Grounded Decision Assistant | ![Assistant](demo/screenshots/05-decision-assistant.png) |

---

## ⚠️ Known Limitations & Synthetic Data Disclaimer

> **Synthetic Demonstration Dataset Disclaimer:**  
> The demonstration dataset used by Nexora is synthetic and is intended for hackathon demonstration purposes (generated with fixed seed 42). It does not represent confidential or proprietary semiconductor manufacturing data.

- **Geopolitical Sourcing Factors:** Uses a structured regional risk factor model based on synthetic concentration rather than a live external geopolitical news API.
- **Fab Equipment Telemetry:** Chamber health and queue values are ingested from synthetic discrete-event log tables rather than direct SECS/GEM fab protocols.

---

## 🏅 What We're Most Proud Of

1. **Real IBM Bob Integration via MCP:** 8 native MCP tools allowing IBM Bob to directly query live fab telemetry, run What-If simulations, and synthesize explainable mitigations without duplicating backend code.
2. **Zero Black-Box Obscurity:** Every single risk score and ML prediction is 100% explainable, showing exact mathematical weights, capacity ratios, lead-time factors, and physics-based drivers.
3. **Interactive What-If Simulation Engine:** Fab operators can dynamically test multi-day supplier outages or equipment failures and instantly receive Before vs. After metric diffs, financial SLA exposure, and actionable mitigation protocols.
4. **Rigorous Test Coverage:** 52 passing unit, integration, and MCP tests verifying all calculations, risk classifications, ML models, simulations, and tool discovery.
