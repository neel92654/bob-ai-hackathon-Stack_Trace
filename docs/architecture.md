# Architecture: Nexora Platform

## System Architecture

```mermaid
graph TD
    subgraph Bob_Agent [AI Agent Layer - IBM Bob]
        BOB[IBM Bob AI Agent / MCP Client]
    end

    subgraph MCP_Layer [Model Context Protocol Server]
        MCP[Nexora MCP Server - mcp-server/server.py]
        T1[get_fab_bottlenecks]
        T2[get_bottleneck_details]
        T3[get_supplier_risk]
        T4[get_supplier_details]
        T5[get_production_impact]
        T6[run_disruption_simulation]
        T7[get_recommendations]
        T8[get_executive_summary]
        MCP --- T1 & T2 & T3 & T4 & T5 & T6 & T7 & T8
    end

    subgraph UI_Layer [Frontend Layer - React 18 + Vite]
        A1[Executive Dashboard]
        A2[Fab Bottleneck View]
        A3[Supply Chain & SPoF View]
        A4[Production Lots View]
        A5[What-If Simulator]
        A6[Recommendation Panel]
        A7[Decision Assistant Console]
    end

    subgraph API_Gateway [Backend Layer - Python Flask REST API]
        B1[Dashboard Blueprint /api/dashboard]
        B2[Bottleneck Blueprint /api/bottlenecks]
        B3[Supplier Blueprint /api/suppliers]
        B4[Production Blueprint /api/production]
        B5[Simulation Blueprint /api/simulation]
        B6[Recommendation Blueprint /api/recommendations]
        B7[Assistant Blueprint /api/assistant]
    end

    subgraph Analytics_Engines [Analytics & ML Engine Layer]
        C1[Bottleneck Calculation Engine]
        C2[5-Factor Supplier Scoring Engine]
        C3[RandomForest Delivery Delay Predictor]
        C4[Deterministic Physics Fallback]
        C5[What-If Disruption Simulation Engine]
        C6[Condition-Driven Recommendation Synthesizer]
        C7[Grounded Decision Assistant Engine]
    end

    subgraph Storage_Layer [Data & Storage Layer]
        D1[(SQLite Database - nexora.db)]
        D2[delivery_model.joblib & model_metrics.json]
        D3[Synthetic CSV Datasets - Seed 42]
    end

    BOB -->|Local STDIO Transport / JSON-RPC| MCP
    MCP -->|Direct Service Invocations| Analytics_Engines
    MCP -->|SQL Queries| Storage_Layer

    UI_Layer -->|HTTP / JSON REST API| API_Gateway
    API_Gateway --> Analytics_Engines
    Analytics_Engines -->|SQL Queries| Storage_Layer
    C3 -->|Model Inference| D2
    C5 -->|Scenario Recalculation| C1
    C5 -->|Scenario Recalculation| C2
    C5 -->|Scenario Recalculation| C3
    C6 -->|Evaluates Risk State| C1
    C6 -->|Evaluates Risk State| C2
    C7 -->|Grounded Telemetry Context| Storage_Layer
```

---

## IBM Bob + MCP Integration Architecture

Nexora exposes its operational intelligence capabilities through a standards-compliant **Model Context Protocol (MCP)** server over local **STDIO transport**.

```mermaid
sequenceDiagram
    autonumber
    actor User as Operations Lead
    participant Bob as IBM Bob (MCP Client)
    participant MCP as Nexora MCP Server (server.py)
    participant Services as Nexora Analytics Services
    participant DB as SQLite / ML Models

    User->>Bob: "Simulate a 14-day disruption of the highest-risk supplier."
    Note over Bob: Discovers run_disruption_simulation tool via MCP
    Bob->>MCP: CallTool(run_disruption_simulation, {scenario_type: 'supplier_disruption', target_id: 'SUP-002', duration_days: 14})
    MCP->>Services: simulate_disruption('supplier_disruption', 'SUP-002', 14)
    Services->>DB: Query supplier lead times, route dependencies, wafer lots
    Services->>Services: Compute ML delay drift & financial SLA risk
    Services-->>MCP: Return structured before/after diff & recommendations
    MCP-->>Bob: Return JSON payload with simulation results
    Bob-->>User: Synthesizes grounded executive briefing with exact metrics
```

---

## What-If Disruption Simulation Data Flow

```mermaid
sequenceDiagram
    autonumber
    actor Operator as Fab Operator
    participant UI as React Simulator UI
    participant API as Flask Simulation API
    participant Engine as Simulation Engine
    participant ML as ML Delay Predictor
    participant Recs as Recommendation Engine
    participant DB as SQLite DB

    Operator->>UI: Selects scenario (e.g. SUP-002 Disrupted for 14 Days)
    Operator->>UI: Clicks [RUN DISRUPTION SIMULATION]
    UI->>API: POST /api/simulation/run {scenario_type, params}
    API->>Engine: simulate_disruption(scenario_type, params)
    Engine->>DB: Fetch baseline supplier, affected processes, queued lots
    Engine->>Engine: Compute simulated dependency spike & lead time shock
    Engine->>ML: Predict delay increase across affected production lots
    Engine->>Engine: Calculate business financial SLA exposure ($)
    Engine->>Recs: Synthesize targeted mitigation actions
    Engine-->>API: Return {baseline, simulated, delta, recommendations}
    API-->>UI: 200 OK with Before vs After Diff JSON
    UI-->>Operator: Displays side-by-side metric diffs & action protocol
```

---

## Components Breakdown

| Component | Technology | Responsibility |
|---|---|---|
| **IBM Bob Client** | IBM Bob Agent | Discovers and invokes MCP tools locally to answer operational queries and simulate scenarios. |
| **Nexora MCP Server** | Python `mcp` SDK, STDIO | Implements 8 native MCP tools exposing bottleneck, supplier, delivery, and simulation intelligence. |
| **Frontend UI** | React 18, Vite, Lucide Icons | Responsive industrial operations console, interactive process flow visualizer, drilldown modals, and simulation dashboards. |
| **API Gateway** | Flask 3.0, Flask-CORS | REST routing, JSON payload validation, error formatting, and CORS management on port 5001. |
| **Bottleneck Engine** | Python (`calculations.py`, `bottleneck_service.py`) | Computes tool utilization percentage, queue pressure, risk tiering (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), and downstream stage starvation paths. |
| **Supplier Risk Engine** | Python (`supplier_risk_service.py`) | 5-factor weighted risk scoring (0–100), automated Single-Point-of-Failure (SPoF) detection, and country concentration metrics. |
| **Delivery ML Pipeline** | scikit-learn (`RandomForestRegressor`), Pandas, NumPy | Trains on historical fab delay logs ($R^2 = 0.954$, MAE = 2.81h), generates predictions with feature importance attribution, and provides deterministic physics fallback. |
| **Simulation Engine** | Python (`simulation_service.py`) | Dispatches and calculates outcomes for 4 disruption scenarios (Supplier Disruption, Tool Outage, Capacity Loss, Demand Surge) with Before vs. After diffs. |
| **Recommendation Engine** | Python (`recommendation_service.py`) | Evaluates active system conditions and synthesizes prioritized, explainable operational response protocols. |
| **Decision Assistant** | Python (`assistant_service.py`) | Grounded natural-language query parser answering questions strictly using verified database facts with supporting reasoning. |
| **Database** | SQLite (`nexora.db`) | Local ACID-compliant database storing equipment, lots, suppliers, process routes, disruptions, and historical delays. |

---

## Data Flow & Processing Lifecycle

1. **Ingestion & In-Memory Hydration:** On initialization or request, SQL queries extract active equipment statuses, lot positions, and supplier dependency shares.
2. **Dynamic Metric Calculation:** Pure functions in `src/backend/utils/calculations.py` compute utilization, queue pressure, and weighted risk scores without modifying the persistent store.
3. **ML Feature Assembly:** For each lot, operational attributes (nominal capacity, WIP queue size, priority number, remaining process stages, chamber health) are transformed into a feature DataFrame and evaluated by `RandomForestRegressor`.
4. **Prescriptive Synthesis:** The recommendation engine checks active bottleneck tiers and SPoF flags, generating prioritized mitigations with operational rationales.
5. **Dual Interface Consumption:**
   - **Visual Dashboard:** The React frontend displays interactive flows, KPI cards, Before/After simulation diffs, and filterable tables.
   - **Agent Interface (IBM Bob):** IBM Bob invokes native MCP tools over STDIO, receiving structured JSON to reason over live operations.

---

## Security & Reliability Considerations

- **Zero Hard-Coded Credentials:** All configuration is managed via `.env.example` and environment variables; `.env` is ignored in Git.
- **Local STDIO Transport:** The MCP server communicates via process pipes without exposing open network ports or requiring remote authentication.
- **Strict Input Validation:** All API endpoints and MCP tool handlers validate incoming parameters and return structured HTTP status codes / error strings without crashing.
- **Offline-First Resilience:** The core application runs locally with zero external API dependencies, guaranteeing complete reproducibility for evaluation.

