# Nexora Application Screenshots

This directory contains high-resolution demonstration screenshots of the running **Nexora** platform.

---

## Screenshot Directory

### `01-dashboard.png` — Executive Operational Overview
![Executive Dashboard](01-dashboard.png)
- **Description:** Real-time operational overview featuring the Overall Fab Risk score, active bottleneck count, high-risk suppliers, interactive 10-stage fab process flow ribbon, top critical tool table, and live disruption alerts.

---

### `02-bottleneck-analysis.png` — Fab Bottleneck Intelligence
![Bottleneck Intelligence](02-bottleneck-analysis.png)
- **Description:** Equipment grid with live capacity utilization progress meters ($\text{WIP} / \text{Capacity} \times 100$), queue pressure metrics, chamber health indicators, downstream stage starvation warnings, and click-to-audit drilldowns.

---

### `03-supplier-risk.png` — Supply Chain SPoF & Geopolitical Concentration
![Supply Chain Risk](03-supplier-risk.png)
- **Description:** Dedicated Single-Point-of-Failure (SPoF) alert cards (highlighting critical suppliers like `SUP-002` Gallium and `SUP-004` Neon Gas), regional geopolitical sourcing concentration analysis, and transparent 5-factor weighted scoring table.

---

### `04-what-if-simulation.png` — What-If Disruption Simulator
![What-If Simulator](04-what-if-simulation.png)
- **Description:** Interactive multi-scenario simulation engine demonstrating a 14-day outage of `SUP-002`, rendering Before vs. After metric comparisons (delay drift $+236.4$h, 38 impacted lots, $\$2.4\text{M}$ business SLA exposure), and prescriptive response mitigation actions.

---

### `05-decision-assistant.png` — Grounded Operational Decision Assistant
![Decision Assistant](05-decision-assistant.png)
- **Description:** Conversational decision support console responding to complex operational queries (*"Why is CVD-03 critical?"*) with direct answers, supporting operational facts, physical reasoning, and recommended line dispatch actions.

---

### `06-bob-mcp-integration.png` — IBM Bob MCP Agent Integration Overview
![IBM Bob MCP Overview](06-bob-mcp-integration.png)
- **Description:** IBM Bob connecting to Nexora via Model Context Protocol (MCP), discovering the 8 registered fab operational tools, and ingesting live telemetry across sequential fab stages.

---

### `07-bob-mcp-bottleneck-query.png` — IBM Bob Bottleneck & SPoF Analysis Tool Execution
![IBM Bob Bottleneck Query](07-bob-mcp-bottleneck-query.png)
- **Description:** IBM Bob executing `get_fab_bottlenecks` and `get_supplier_risk` tools to diagnose tool overloads on `CVD-03` and Single-Point-of-Failure risks on `SUP-002`.

---

### `08-bob-mcp-simulation-actions.png` — IBM Bob What-If Disruption Simulation & Mitigation
![IBM Bob Simulation Actions](08-bob-mcp-simulation-actions.png)
- **Description:** IBM Bob invoking `run_disruption_simulation` to stress-test a 14-day supplier outage and synthesizing prioritized, condition-driven mitigation action plans.
