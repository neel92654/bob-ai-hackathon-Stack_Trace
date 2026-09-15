# Nexora Model Context Protocol (MCP) Server

> **IBM Bob AI Innovation Hackathon 2026**  
> **Track:** AI (Problem Statement S2: Fab Bottleneck & Supply Chain Risk Advisor)

This directory contains the **Nexora MCP Server**, which exposes Nexora's semiconductor fab bottleneck diagnostics, single-point-of-failure supplier scoring, machine learning delivery delay predictions, and What-If disruption simulations as standard Model Context Protocol (MCP) tools for **IBM Bob**.

---

## 🏛️ Architecture

```
IBM Bob (MCP Client / Agent)
      │
      ▼ (STDIO Transport / JSON-RPC)
Nexora MCP Server (mcp-server/server.py)
      │
      ▼ (Direct Python Service Invocations — Zero Logic Duplication)
Nexora Analytics & Decision Services
      │
      ├── Bottleneck Intelligence (WIP Queue Ratios & Process Starvation)
      ├── 5-Factor Supplier Risk Scoring (0–100 & SPoF Detection)
      ├── RandomForest ML Delivery Delay Engine (R² = 0.954)
      ├── What-If Disruption Simulation Engine (4 Scenarios)
      └── Condition-Driven Recommendation Synthesizer
      │
      ▼
SQLite Database (nexora.db) & Serialized ML Model (delivery_model.joblib)
```

---

## 🛠️ Exposed MCP Tools

| # | Tool Name | Parameters | Description |
|---|---|---|---|
| 1 | `get_fab_bottlenecks` | `severity` (optional: 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW') | Retrieves all fab tool bottlenecks with capacity utilization %, WIP load, severity tier, explainable diagnosis, and affected lot counts. |
| 2 | `get_bottleneck_details` | `tool_id` (required, e.g. `'CVD-03'`) | Retrieves deep-dive diagnostics for a specific equipment tool, chamber health, MTBF, downstream process starvation paths, and assigned wafer lots. |
| 3 | `get_supplier_risk` | `min_risk_level` (optional) | Retrieves explainable 5-factor supplier risk scores (0–100), single-point-of-failure (SPoF) flags, lead times, and geopolitical sourcing concentration. |
| 4 | `get_supplier_details` | `supplier_id` (required, e.g. `'SUP-002'`) | Retrieves detailed risk profiling, factor weight breakdowns, alternate supplier availability %, and affected fab process stages. |
| 5 | `get_production_impact` | `lot_id`, `priority`, `process_id` (all optional) | Retrieves wafer lot tracking across 10 manufacturing stages with ML-predicted delivery delay hours, revised completion dates, and order urgency scores. |
| 6 | `run_disruption_simulation` | `scenario_type`, `target_id`, `duration_days`, etc. | Executes a What-If disruption simulation (Supplier Disruption, Tool Breakdown, Capacity Derating, Demand Surge), returning Before vs. After metric diffs and SLA exposure. |
| 7 | `get_recommendations` | `category`, `priority` (all optional) | Retrieves prioritized prescriptive mitigations generated from live bottleneck conditions, SPoF exposures, and active disruptions. |
| 8 | `get_executive_summary` | *(none)* | Retrieves a structured high-level executive summary of overall fab risk, critical bottlenecks, high-risk suppliers, affected lots, and top mitigations. |

---

## ⚡ Running the MCP Server Locally

### 1. Install Dependencies
```bash
pip install -r mcp-server/requirements.txt
```

### 2. Start MCP Server (STDIO Mode)
```bash
python3 mcp-server/server.py
```

---

## 🤖 IBM Bob Configuration

To enable IBM Bob to discover and invoke Nexora's MCP tools, add the following to your project's `.bob/mcp.json`:

```json
{
  "mcpServers": {
    "nexora": {
      "command": "python3",
      "args": ["mcp-server/server.py"],
      "cwd": "${workspaceFolder}"
    }
  }
}
```
