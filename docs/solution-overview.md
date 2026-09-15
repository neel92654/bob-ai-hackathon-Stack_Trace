# Solution Overview: Nexora — Operational Risk & Supply Intelligence Platform

## What We Built

**Nexora** is an explainable operational risk and supply intelligence platform developed for the **IBM Bob AI Innovation Hackathon 2026** (Problem Statement S2: *Fab Bottleneck & Supply Chain Risk Advisor*). 

Nexora bridges the gap between semiconductor fab floor physics and global supply chain logistics by answering five fundamental operational questions:
1. **WHERE is the operational bottleneck?** (Pinpoints specific tools operating above rated capacity).
2. **HOW severe is the bottleneck?** (Computes queue utilization % and classifies into 4 explainable risk tiers: LOW, MEDIUM, HIGH, CRITICAL).
3. **WHAT downstream production/delivery impact can it cause?** (Predicts delivery delay hours across active wafer lots using an interpretable `RandomForestRegressor` ML model).
4. **WHICH suppliers represent critical supply-chain risk?** (Detects Single-Point-of-Failure suppliers and geopolitical concentration using an explainable 5-factor weighted scoring model).
5. **WHAT SHOULD an operator do about the identified risk?** (Generates condition-driven, prioritized mitigation protocols and simulates What-If disruption scenarios before committing changes).

---

## How It Works

```
[Fab Telemetry & WIP Queues] ──┐
                               ├──► [Analytics & Scoring Engine] ──► [ML Delivery Model (R²=0.95)]
[Supplier & SPoF Database]   ──┘              │                                 │
                                              ▼                                 ▼
                                    [What-If Simulator] ────────► [Prescriptive Recommendations]
                                              │                                 │
                                              └────────► [Decision Assistant] ◄─┘
```

1. **Continuous Data Ingestion:** Ingests equipment nominal capacities, active WIP queues, chamber health metrics, production lots, and supplier dependency profiles into a centralized SQLite database.
2. **Bottleneck Severity Computation:** Calculates tool capacity utilization ($\text{Utilization} = \text{WIP} / \text{Capacity} \times 100$) and queue pressure, mapping downstream process stage dependencies across 10 sequential fab steps.
3. **Explainable Supplier Risk Scoring:** Computes a normalized 0–100 risk score based on Market Dependency (30%), Lead Time (25%), Material Criticality (20%), Geopolitical Risk (15%), and Alternate Supplier Availability (10%). Automatically flags suppliers with $\ge 75\%$ dependency and no secondary backup as Single Points of Failure (SPoF).
4. **ML Delivery Delay Forecasting:** Runs an interpretable `RandomForestRegressor` model (trained on historical cycle data with $R^2 = 0.954$) to project delivery schedule drift for each wafer lot, ranking orders by urgency.
5. **What-If Disruption Simulation:** Allows operators to test 4 disruption scenarios (Supplier Disruption, Equipment Outage, Capacity Derating, and Demand Surge), producing immediate Before vs. After metrics diffs and business exposure calculations.
6. **Prescriptive Action Synthesis:** Generates prioritized operational response recommendations with specific actions, operational justifications, and expected benefits.
7. **Grounded Decision Assistant:** Provides a natural-language Q&A console strictly grounded in verified database facts to support line managers in rapid decision-making.

---

## Key Design Decisions

| Decision | Rationale |
|---|---|
| **Deterministic Data Generation (Seed: 42)** | Guarantees 100% reproducibility of the demonstration dataset across equipment, lots, suppliers, and historical logs without requiring access to confidential fab data. |
| **Explainable ML (RandomForestRegressor)** | Provides verified predictive accuracy ($R^2 = 0.954$, MAE = 2.81h) while allowing transparent feature importance attribution, avoiding uninterpretable black-box neural networks. |
| **Strict Fallback Physics Engine** | If the ML model artifact is unavailable, the system automatically falls back to deterministic fab queue formulas with zero fabrication. |
| **Interactive What-If Simulation Engine** | Enables proactive stress-testing of multi-day outages and embargos with Before vs. After metric diffs, preventing costly unsimulated operational decisions. |
| **Grounded Decision Assistant** | Enforces strict fact-grounding so the assistant only answers using tracked database records and states when information is unavailable. |

---

## IBM Bob Integration via Model Context Protocol (MCP)

**IBM Bob** acts as the AI Agent / MCP Client that interacts with Nexora. Rather than faking a proprietary REST API or adding unverified model dependencies, Nexora implements a native **Model Context Protocol (MCP)** server (`mcp-server/server.py`) over local **STDIO transport**.

### Architecture Principle:
```
IBM Bob (MCP Client / Agent)
     │
     ▼ (Local STDIO / JSON-RPC)
Nexora MCP Server (mcp-server/server.py)
     │
     ▼ (Direct Service Invocations / Internal APIs)
Nexora Backend Analytics & ML Pipeline
     │
     ▼
SQLite Database (nexora.db) + RandomForest ML Model
```

### Exposed MCP Tools:

1. `get_fab_bottlenecks`:
   - *Description:* Retrieves Nexora's current semiconductor fabrication bottlenecks. Use this when the user asks which fab tools or process stages are currently constraining production.
   - *Returns:* Tool ID, process stage, utilization %, WIP count, capacity, severity tier, and physical bottleneck reason.
2. `get_bottleneck_details`:
   - *Description:* Retrieves in-depth telemetry and queued lot drilldown for a specific fabrication tool.
   - *Parameters:* `tool_id` (e.g., `CVD-03`, `ETCH-01`).
3. `get_supplier_risk`:
   - *Description:* Returns complete supplier risk rankings, single-point-of-failure (SPoF) detections, and country concentration metrics.
4. `get_supplier_details`:
   - *Description:* Retrieves granular risk breakdown, lead times, materials provided, and dependency metrics for a specific supplier.
   - *Parameters:* `supplier_id` (e.g., `SUP-002`).
5. `get_production_impact`:
   - *Description:* Evaluates downstream production and delivery schedule delay impact for a specific wafer lot using ML forecasting.
   - *Parameters:* `lot_id` (e.g., `LOT-8001`).
6. `run_disruption_simulation`:
   - *Description:* Executes What-If disruption simulations (supplier disruption, equipment failure, capacity reduction, demand increase) and returns side-by-side Before vs. After metric diffs, delay drift, impacted lots, and financial SLA exposure.
   - *Parameters:* `scenario_type`, `target_id`, `duration_days` or `capacity_reduction`.
7. `get_recommendations`:
   - *Description:* Retrieves prioritized, condition-driven mitigation actions synthesized by Nexora's operational advisory engine.
8. `get_executive_summary`:
   - *Description:* Provides high-level operational risk summary across fab floor health, supply chain SPoFs, production lot delays, and top priority mitigation protocols.

---

## Known Limitations & Future Roadmap

- **Current Prototype:** Uses synthetic demonstration data (Seed: 42) and SQLite for zero-configuration local evaluation.
- **Future Production Roadmap:**
  1. Direct integration with SECS/GEM fab protocols and MES platforms (Applied Materials SmartFactory, Siemens Camstar).
  2. Integration with live maritime AIS shipping feeds and geopolitical trade restriction databases.
  3. Automated dispatch rule push directly into fab automated material handling systems (AMHS).

