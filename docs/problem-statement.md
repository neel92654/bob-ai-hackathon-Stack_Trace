# Problem Statement: S2 — Fab Bottleneck & Supply Chain Risk Advisor

## Background

Semiconductor fabrication facilities (fabs) are among the most capital-intensive and complex manufacturing environments in the world. Modern fabs run hundreds of sequential, high-precision chemical, optical, and mechanical process steps (such as EUV Photolithography, Chemical Vapor Deposition, Plasma Etching, Ion Implantation, and Chemical Mechanical Polishing) across hundreds of multi-million dollar tools operating 24/7.

Because process routes are tightly coupled and wafer lots spend weeks in production, the overall throughput of a fab is governed by its slowest or most congested bottleneck tools. Furthermore, semiconductor manufacturing depends on an ultra-specialized, highly concentrated global supply chain for critical raw materials, precursors, and consumables (e.g., EUV photoresists from Japan, high-purity neon gas from Eastern Europe, and gallium substrates from East Asia).

## The Problem

Fab managers, production dispatchers, and supply chain procurement teams face two intersecting operational crises:

1. **Intra-Fab Queue Volatility & Hidden Bottlenecks:** When a critical tool (such as a CVD reactor or stepper) experiences micro-stoppages or chamber drift, work-in-progress (WIP) lots rapidly accumulate. This causes severe queue back-pressure upstream and starves downstream processing tools. Dispatchers often fail to detect these imbalances until wafer lots have already missed customer SLA commitment windows.
2. **Single-Point-of-Failure (SPoF) Supply Vulnerability:** Many critical semiconductor materials have high supplier dependency shares (>80%) with zero qualified secondary sources and extended procurement lead times (>40 days). A sudden geopolitical export restriction or regional logistics shock halts entire fab process routes without warning.
3. **Fragmented Decision Support & Lack of Simulation:** Existing Fab Manufacturing Execution Systems (MES) and ERP tools are siloed. They display raw historical logs but lack explainable bottleneck scoring, machine-learning-based delivery delay forecasting, and simulation capabilities to test "What happens if Tool X fails for 24 hours?" or "What happens if Supplier Y is unavailable for 14 days?".

## Who is Affected

- **Fab Operations & Line Managers:** Responsible for overall equipment effectiveness (OEE), line balancing, wafer throughput, and preventing chamber bottlenecks.
- **Production Dispatchers & Planners:** Tasked with scheduling high-priority customer lots (Automotive Tier-1, Hyperscale AI, Mobile Flagship) and meeting strict delivery due dates.
- **Procurement & Supply Chain Risk Directors:** Managing raw material inventory, buffer safety stocks, and dual-sourcing strategies across global geographies.
- **Enterprise Semiconductor Executives:** Exposed to millions of dollars in customer SLA penalty clauses, unfulfilled order backlogs, and lost wafer yield.

## Why It Matters

- **Financial Impact:** An unplanned downtime event on a critical bottleneck tool or a material stockout can cost a semiconductor fab between **$100,000 to over $1,000,000 per shift** in idle capacity, scrapped wafers, and missed delivery penalties.
- **Customer Trust & Contractual SLAs:** Hyperscale AI and Tier-1 automotive customers impose severe contractual penalties for late deliveries, causing catastrophic downstream supply chain delays in global automotive and tech industries.
- **Geopolitical Fragility:** As semiconductor supply chains face export controls and regional trade volatility, visibility into single-source supplier dependencies has become an existential business requirement.

## Why Existing Solutions Fall Short

- **Siloed Legacy Systems:** Fab MES tools track machine health, while ERP tools track purchase orders—neither correlates how a supplier delay directly triggers fab queue starvation.
- **Black-Box Metrics:** Existing analytics dashboards output unexplainable risk numbers without explaining the underlying physical capacity ratios or lead-time drivers.
- **Reactive Post-Mortems:** Standard operations reviews occur weekly or monthly after delivery delays have already occurred, rather than providing predictive ML forecasting and real-time What-If disruption simulation.
- **No Prescriptive Mitigations:** Traditional dashboards show that a tool is red, but fail to provide actionable, prioritized mitigation steps (such as lot re-routing, chamber maintenance acceleration, or secondary supplier activation).
