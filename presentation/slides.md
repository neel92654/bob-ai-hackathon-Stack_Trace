# 🚀 Nexora Presentation Slide Deck (8 Slides)

**Track:** AI / Semiconductor  
**Problem Statement S2:** Fab Bottleneck & Supply Chain Risk Advisor  
**Project:** Nexora — Operational Risk & Supply Intelligence Platform  
**Team:** Stack_Trace  

---

## Slide 1: Title & Overview

### 📌 Title & Subtitle:
**NEXORA — Operational Risk & Supply Intelligence Platform**  
*Explainable AI, Physics-Grounded Bottleneck Analytics & Supply Chain Risk Simulator for Semiconductor Fabs*

### 📝 Key Content:
- **Hackathon:** IBM Bob AI Innovation Hackathon 2026
- **Problem Statement:** S2 — Fab Bottleneck & Supply Chain Risk Advisor
- **Team Name:** `Stack_Trace`
- **Team Members:** Neel Patel (Lead), Mayank Padmani, Meet Ramani, Kremil Dobariya
- **🌐 Live Demo URL:** [https://nexora-7cs9.onrender.com/](https://nexora-7cs9.onrender.com/)
- **💻 GitHub Repository:** [https://github.com/neel92654/bob-ai-hackathon-Stack_Trace](https://github.com/neel92654/bob-ai-hackathon-Stack_Trace)
- **📹 Video Demonstration:** Available in `demo/demo-video-link.txt` | Screenshots in `demo/screenshots/`

### 🎯 Core Mission:
Empower semiconductor fab line operators and supply chain planners to pre-empt cascading queue bottlenecks and single-source supplier disruptions using explainable ML, 4-scenario What-If simulations, and IBM Bob via the Model Context Protocol (MCP).

### 🎙️ Speaker Script:
> *"Hello judges! We are Team Stack_Trace. Today we present Nexora — an explainable operational risk and supply intelligence platform developed for Problem Statement S2 of the IBM Bob AI Innovation Hackathon 2026. Nexora bridges semiconductor fab floor physics with global supply chain logistics to prevent multi-million dollar wafer delivery delays and critical material shortages."*

---

## Slide 2: The Problem: Fab Bottlenecks & Supply Shock Fragility

### 📌 Title & Subtitle:
**The High-Stakes Fragility of Modern Semiconductor Fabs**  
*26–52 Week Lead Times, Cascading Queue Back-Pressure & Catastrophic SPoF Materials*

### 📝 Key Content:
- **Ultra-Long Multi-Stage Processing:** Microchip manufacturing spans 10+ strictly sequential stages (Lithography, Etch, CVD, CMP, Ion Implantation, Metrology). A slowdown at one tool creates severe upstream queue back-pressure and starves downstream processing.
- **Extreme Single-Source Raw Material Risks:** Fabs rely on single-source suppliers for critical chemicals and precursors (e.g., China controls >80% of global Gallium and Germanium, currently subject to strict export controls).
- **The $100K+/Hour Outage Cost:** A single unplanned tool outage or chemical stockout costs $100,000–$300,000 per hour in idle capacity and breaches customer SLAs.
- **Lack of Predictive Simulation:** Fab managers cannot test the blast radius of a 14-day supplier embargo or equipment failure before it happens.

### 🎨 Visual Suggestion:
- Sequential wafer flow diagram with a critical red bottleneck at `CVD-03` blocking downstream CMP and Lithography tools.
- Highlight Callout Box: *"Unplanned fab downtime = $100,000–$300,000 / hour"*.

### 🎙️ Speaker Script:
> *"Semiconductor manufacturing is the most complex supply chain on earth. Wafers take up to a year to manufacture through hundreds of steps. If a chemical vapor deposition tool gets backed up, or if a single-source Gallium supplier experiences an export embargo, entire fab lines freeze. Today's fabs cannot afford to discover these risks after production has already stopped."*

---

## Slide 3: Why Existing Approaches Fall Short

### 📌 Title & Subtitle:
**The Industry Gap: Siloed Data, Black-Box AI & Reactive Post-Mortems**

### 📝 Key Content:
| Existing Approach | Critical Limitation | Impact on Semiconductor Fabs |
|---|---|---|
| **Siloed MES & ERP Systems** | MES monitors machine faults; ERP tracks procurement invoices independently. | Zero correlation between supplier lead-time drift and real-time fab queue starvation. |
| **Black-Box AI Models** | Deep neural nets output ungrounded risk percentages without clear drivers. | Operators **refuse to trust or act** on unexplainable machine predictions. |
| **Reactive Post-Mortems** | Delay analysis occurs *after* wafer lots miss customer delivery dates. | Fabs incur massive SLA financial penalties and idle downstream assembly factories. |
| **No Pre-Emptive Simulation** | Line changes are executed live on the floor without impact stress-testing. | Unsimulated re-routing can accidentally shift bottlenecks to more critical tools. |

### 🎨 Visual Suggestion:
- 3 "Pain Point" badges with warning icons: ❌ *Siloed MES/ERP Data*, ❌ *Opaque Black-Box Models*, ❌ *Post-Mortem Reactivity*.

### 🎙️ Speaker Script:
> *"Why don't current systems solve this? Because MES and ERP operate in separate silos. MES knows a tool is down, ERP knows a supplier is late, but neither connects the dots. When traditional AI is added, it outputs black-box numbers that fab operators cannot trust. Line managers are left reacting to crises after millions in customer SLAs are already lost."*

---

## Slide 4: The Nexora Solution

### 📌 Title & Subtitle:
**End-to-End Explainable Operational Intelligence**  
*Answering 5 Fundamental Fab Questions with 100% Mathematical Transparency*

### 📝 Key Content:
Nexora unifies fab queue telemetry and supplier risk into an actionable 5-step decision loop:
1. **WHERE is the bottleneck?** $\rightarrow$ Real-time queue overload detection across all 10 fab process stages.
2. **HOW SEVERE is the risk?** $\rightarrow$ Instant tool capacity utilization ($\frac{\text{WIP}}{\text{Capacity}} \times 100$) in 4 explainable tiers (*Low, Medium, High, Critical*).
3. **WHAT is the downstream delivery impact?** $\rightarrow$ Interpretable ML delivery delay predictions ($R^2 = 0.954$, MAE = 2.81h) per wafer lot.
4. **WHICH suppliers represent critical risks?** $\rightarrow$ Transparent 5-factor scoring (0–100) with automatic Single-Point-of-Failure (SPoF) flags.
5. **WHAT SHOULD an operator do?** $\rightarrow$ Interactive What-If disruption simulations and prescriptive condition-driven mitigation protocols.

### 🎨 Visual Suggestion:
- 5-part circular lifecycle diagram: *Detect $\rightarrow$ Quantify $\rightarrow$ Predict $\rightarrow$ Stress-Test $\rightarrow$ Mitigate*.
- Badge: *"100% Explainable — Zero Black-Box Obscurity"*.

### 🎙️ Speaker Script:
> *"Nexora transforms fab operations by answering the five essential questions every fab director asks: Where is the bottleneck? How severe is it? What will it do to customer deliveries? Which suppliers are vulnerable? And most importantly: What exact actions should we take right now? Every calculation is mathematically grounded and completely transparent."*

---

## Slide 5: Technical Architecture & IBM Bob MCP Integration

### 📌 Title & Subtitle:
**Native Model Context Protocol (MCP) Server for IBM Bob**  
*Full-Stack Industrial Intelligence with Zero Logic Duplication*

### 📝 Key Content:
- **Agentic AI Layer (IBM Bob):** Natural-language conversational interface discovering and invoking 8 native MCP tools via local STDIO transport (`.bob/mcp.json`).
- **Nexora MCP Server (`mcp-server/server.py`):** Exposes core fab analytics, ML predictions, and simulation endpoints directly to IBM Bob over JSON-RPC.
- **Backend & ML Engine (Python Flask):** Service layer housing the `RandomForestRegressor` ML model, feature attribution pipeline, and physics fallback engine.
- **Data & Telemetry Layer (SQLite):** Seeded with realistic 10-stage semiconductor fab routing, equipment WIP queues, and supplier dependency graphs (Seed: 42).
- **Industrial Dashboard (React 18 + Vite):** High-density glassmorphism UI with real-time progress meters, interactive simulators, and telemetry consoles.

### 🎨 Visual Suggestion (Architecture Diagram):
```
IBM Bob (MCP Client / Agent)
      │
      ▼ (STDIO Transport / JSON-RPC via .bob/mcp.json)
Nexora MCP Server (8 Native Tools)
      │
      ▼ (Reuses existing analytics & ML services — zero duplication)
Backend Analytics & RandomForestRegressor ML Engine (R² = 0.954)
      │
      ▼
SQLite Database (nexora.db) + Telemetry Datasets
```

### 🎙️ Speaker Script:
> *"Our architecture is purpose-built for IBM Bob. Rather than mocking an API, we implemented a real Model Context Protocol server over STDIO. When you ask Bob a question, Bob invokes our 8 native MCP tools to query live fab telemetry, run What-If simulations, and return fact-grounded operational guidance without hallucinations."*

---

## Slide 6: Fab Bottleneck & Supplier SPoF Intelligence

### 📌 Title & Subtitle:
**Physics-Based Queue Analytics & Explainable 5-Factor Supplier Scoring**  
*Real-Time Capacity Progress Meters & Automated Single-Point-of-Failure Detection*

### 📝 Key Content:
- **Fab Equipment Bottleneck Engine:**
  - $\text{Capacity Utilization (\%)} = \left(\frac{\text{Active WIP Queue}}{\text{Rated Capacity}}\right) \times 100$
  - 4-Tier Explainable Severity: **LOW (<70%)**, **MEDIUM (70–84%)**, **HIGH (85–99%)**, **CRITICAL ($\ge 100\%$)**.
  - Example: `CVD-03` running at **130% utilization** (65 WIP vs 50 capacity) triggering upstream back-pressure and downstream CMP starvation.
- **Explainable 5-Factor Supplier Risk Scoring (0–100):**
  $$\text{Score} = (0.30 \times \text{Dep}) + (0.25 \times \text{LeadTime}) + (0.20 \times \text{Criticality}) + (0.15 \times \text{GeoRisk}) + (0.10 \times \text{AltGap})$$
- **Automated SPoF Detection:** Instantly flags suppliers with **$\ge 75\%$ dependency** and **0 qualified secondary sources** (e.g., `SUP-002`, Sino Rare Earths — 85% Gallium supply).

### 🎨 Visual Suggestion:
- Embed screenshot from [`demo/screenshots/02-bottleneck-analysis.png`](../demo/screenshots/02-bottleneck-analysis.png) and [`demo/screenshots/03-supplier-risk.png`](../demo/screenshots/03-supplier-risk.png).

### 🎙️ Speaker Script:
> *"On the fab floor, Nexora monitors every tool's queue ratio in real time, grading risk across 4 transparent tiers. At the same time, our supply chain engine calculates normalized 0 to 100 risk scores across 5 weighted factors. If a single supplier provides 85% of our Gallium with no backup, Nexora immediately flags them as an active Single Point of Failure."*

---

## Slide 7: What-If Disruption Simulator & ML Forecasting

### 📌 Title & Subtitle:
**Interactive 4-Scenario Stress-Testing & ML Delivery Delay Forecasting**  
*Predictive Precision ($R^2 = 0.954$) with Before vs. After Metric Diffs & Financial SLA Exposure*

### 📝 Key Content:
- **Interpretable Machine Learning Engine:**
  - `RandomForestRegressor` predicting delivery delay in hours for each active wafer lot.
  - **$R^2 = 0.954$** | **MAE = 2.81 hours** on 500+ hour fab cycles.
  - Validated Feature Attribution: Queue Latency (38%), Bottleneck Severity (29%), Sourcing Drift (19%), Chamber Health (14%).
  - **Deterministic Physics Fallback:** Ensures 100% platform uptime if ML models are offline.
- **4 Disruption Simulation Scenarios:**
  1. **Supplier Embargo** (e.g., `SUP-002` Gallium halted for 14 days)
  2. **Equipment Breakdown** (e.g., `CVD-03` outage for 48 hours)
  3. **Capacity Derating** (e.g., Cleanroom cooling failure -30%)
  4. **Demand Surge** (e.g., +50% urgent priority lot injection)
- **Quantified Business Exposure:** Computes Before vs. After delay drift (e.g., **$+236.4\text{h}$**), affected wafer lots, and SLA financial penalties (e.g., **$\$2.4\text{M}$** at risk).

### 🎨 Visual Suggestion:
- Embed screenshot from [`demo/screenshots/04-what-if-simulation.png`](../demo/screenshots/04-what-if-simulation.png) showing the interactive simulation controls, Before vs. After metrics, and SLA exposure card.

### 🎙️ Speaker Script:
> *"Our What-If Disruption Simulator is Nexora's key differentiator. Before an operator makes a costly floor change, they can simulate a 14-day Gallium embargo or an equipment breakdown. Nexora forecasts the delivery delay drift with an $R^2$ of 0.954, calculates the exact multi-million dollar SLA exposure, and generates a pre-validated mitigation plan."*

---

## Slide 8: IBM Bob Integration, Impact & Roadmap

### 📌 Title & Subtitle:
**Condition-Driven Prescriptive Protocols, Production Readiness & Future Vision**  
*52 Automated Tests Passing, Demonstrated Business ROI & Industrial Roadmap*

### 📝 Key Content:
- **Prescriptive Condition-Driven Mitigations:**
  - Dynamically synthesized protocols with clear **Actions**, **Operational Rationales**, and **Expected Benefits** (e.g., Reroute non-critical lots to `CVD-01`, qualify backup source `SUP-003`).
- **Grounded Decision Assistant:** Natural-language conversational console powered by IBM Bob, strictly grounded in verified database telemetry with zero hallucination.
- **Production Readiness & Verification:**
  - **52 Automated Tests Passing** (`pytest tests/ -v`) covering ML inference, queue formulas, simulations, and MCP tools.
  - 100% reproducible synthetic dataset (Seed: 42).
- **Quantified Business Impact & Future Roadmap:**
  - ⚡ **90% Faster Bottleneck Triage:** Seconds vs. hours of manual MES cross-referencing.
  - 💰 **Millions in Avoided SLA Penalties:** Early SPoF mitigation prevents multi-week fab shutdowns.
  - 🗺️ **Roadmap:** Direct SECS/GEM fab connectivity, live maritime AIS shipping feeds, and Automated Material Handling System (AMHS) dispatch integration.

### 🎨 Visual Suggestion:
- Embed screenshot from [`demo/screenshots/05-decision-assistant.png`](../demo/screenshots/05-decision-assistant.png).
- Badges: `52/52 Tests Passed`, `IBM Bob Integrated`, `Live on Render`.

### 🎙️ Speaker Script:
> *"In summary, Nexora turns complex fab telemetry and supply chain risks into actionable, explainable operational intelligence. With 52 passing automated tests, real IBM Bob MCP integration, and verified business ROI, Nexora empowers semiconductor fabs to stay ahead of disruptions. Thank you!"*

---

## 📋 Summary Table for Quick Reference

| Slide | Core Focus | Key Highlight / Data Point |
|---|---|---|
| **1. Title & Overview** | Team & Track Introduction | Live Render Demo & GitHub Repository Links |
| **2. The Problem** | Fab Bottlenecks & Supply Shock | 26–52 week lead times; $100K+/hr downtime costs |
| **3. Existing Gaps** | MES/ERP Silos & Black Boxes | Uncorrelated data, ungrounded AI, reactive post-mortems |
| **4. The Solution** | 5 Fundamental Fab Questions | Detect $\rightarrow$ Quantify $\rightarrow$ Predict $\rightarrow$ Stress-Test $\rightarrow$ Mitigate |
| **5. Architecture** | IBM Bob MCP Integration | 8 Native Tools over local STDIO transport |
| **6. Bottleneck & Supply** | Utilization & 5-Factor Score | (WIP/Capacity)*100; SPoF detection for $\ge 75\%$ dependency |
| **7. What-If Simulator** | ML Forecasting & Simulations | $R^2 = 0.954$, MAE = 2.81h; $+236.4\text{h}$ delay drift & $\$2.4\text{M}$ SLA exposure |
| **8. Impact & Roadmap** | Prescriptive Protocols & Vision | 52/52 tests passing; 90% faster triage; SECS/GEM roadmap |
