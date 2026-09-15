# Nexora Slide Deck Presentation

## Slide 1: Title
**NEXORA**
*Operational Risk & Supply Intelligence Platform*
IBM Bob AI Innovation Hackathon 2026 | Problem Statement S2: Fab Bottleneck & Supply Chain Risk Advisor
**Team:** Stack_Trace | **Lead:** Neel Patel

---

## Slide 2: The Core Industry Challenge
- Semiconductor fabs operate tightly coupled, 24/7 manufacturing lines with hundreds of sequential process stages.
- Tool WIP queue overloading creates severe upstream back-pressure and starves downstream processing.
- Single-source chemical & raw material suppliers (>80% dependency, no backup) leave fabs vulnerable to multi-million dollar outages.

---

## Slide 3: Why Existing Approaches Fail
- **Siloed Systems:** MES tracks machine errors; ERP tracks invoices. Neither correlates supplier delays with fab queue starvation.
- **Black-Box Metrics:** Complex deep learning models output uninterpretable risk scores that operators cannot trust.
- **Reactive Post-Mortems:** Line managers analyze delivery failures *after* customer SLAs are breached.

---

## Slide 4: The Nexora Solution
Nexora bridges fab physics with supply chain logistics by answering 5 fundamental questions:
1. **WHERE** is the bottleneck? (Tool-level WIP queue detection)
2. **HOW SEVERE** is the risk? (Utilization % & 4-tier explainable rating)
3. **WHAT IMPACT** will it cause? (ML predicted delivery delay hours, $R^2 = 0.954$)
4. **WHICH SUPPLIERS** are vulnerable? (5-factor scoring & SPoF detection)
5. **WHAT SHOULD WE DO?** (Condition-driven mitigation protocols & What-If simulation)

---

## Slide 5: System Architecture & IBM Bob MCP Server
- **Dual Consumption Layers:**
  - **Visual Frontend:** React 18 + Vite with an industrial glassmorphism design system.
  - **AI Agent Interface:** Native **Model Context Protocol (MCP)** server over local STDIO transport for IBM Bob.
- **Backend Services:** Modular Python Flask REST API & service layer with 7 dedicated domain engines.
- **ML Engine:** Interpretable `RandomForestRegressor` with feature importance attribution & physics fallback.
- **Storage:** Local SQLite database (`nexora.db`) seeded with realistic semiconductor manufacturing datasets (Seed 42).

---

## Slide 6: Bottleneck & Supply Chain Intelligence
- **Fab Bottlenecks:** Real-time capacity utilization ($\text{WIP} / \text{Capacity} \times 100$), queue pressure meters, and 10-stage sequential flow starvation mapping.
- **Supplier Risk:** Explainable weighted scoring (Dependency 30%, Lead Time 25%, Criticality 20%, Geopolitical 15%, Alternate 10%) with automated SPoF flags.

---

## Slide 7: What-If Disruption Simulator (Key Differentiator)
- Stress-tests multi-day supplier embargos (e.g., `SUP-002` Gallium for 14 days) and equipment breakdowns (`CVD-03` for 24h).
- Computes side-by-side **Before vs. After** metric diffs: delay drift ($+236.4$h), impacted wafer lots, and financial SLA exposure ($\$2.4\text{M}$).
- Automatically synthesizes prioritized response mitigation protocols.

---

## Slide 8: Real IBM Bob + MCP Integration
- **8 Native MCP Tools:** Exposes fab bottlenecks, lot delivery impact, supplier SPoF detection, What-If simulation, and executive summaries.
- **No Faked APIs / No Hallucinations:** Bob invokes real tools over STDIO, receiving verified JSON metrics from SQLite & ML models.
- **Zero Black-Box Obscurity:** 100% explainability across all risk scores and predictions.
- **Tested & Verified:** 52 automated unit/integration/MCP tests passing with 100% structural CI compliance.

