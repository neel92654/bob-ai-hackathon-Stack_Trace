# Presentation Deck: Nexora

This directory contains the presentation outline and slide structure for **Nexora — Operational Risk & Supply Intelligence Platform** (IBM Bob AI Innovation Hackathon 2026, Problem S2).

---

## Slide Deck Overview (8 Slides)

- **Slide 1: Title & Overview** — *Nexora: Operational Risk & Supply Intelligence Platform* (IBM Bob AI Hackathon 2026, Problem Statement S2).
- **Slide 2: The Problem** — Fab bottleneck congestion, queue back-pressure, single-point-of-failure supplier exposure, and lack of simulation tools.
- **Slide 3: Why Existing Approaches Fall Short** — Siloed MES/ERP tools, black-box opaque metrics, reactive post-mortems, and zero pre-emptive simulation.
- **Slide 4: The Nexora Solution** — End-to-end explainable intelligence answering *Where*, *How Severe*, *What Impact*, *Which Suppliers*, and *What Action*.
- **Slide 5: Technical Architecture** — React 18 frontend + Python Flask REST API + SQLite + Interpretable `RandomForestRegressor` ML ($R^2 = 0.954$).
- **Slide 6: Fab Bottleneck & SPoF Intelligence** — Live capacity utilization progress meters, 10-stage process flow starvation mapping, and 5-factor explainable supplier risk scoring.
- **Slide 7: What-If Disruption Simulator** — Proactive discrete-event simulation of supplier embargoes and equipment outages with Before vs. After metric diffs and financial SLA risk.
- **Slide 8: IBM Bob Integration & Impact** — Grounded decision assistant reasoning, prescriptive condition-driven mitigations, and roadmap.

*For complete slide notes and text, see [`slides.md`](slides.md).*
