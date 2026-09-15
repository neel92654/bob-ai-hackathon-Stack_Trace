# Presentation Deck: Nexora

This directory contains the presentation outline, slide deck structure, and slide-by-slide speaker notes for **Nexora — Operational Risk & Supply Intelligence Platform** (IBM Bob AI Innovation Hackathon 2026, Problem Statement S2: *Fab Bottleneck & Supply Chain Risk Advisor*).

---

## 🔗 Quick Links & Submission Artifacts
- **Live Demo URL:** [https://nexora-7cs9.onrender.com/](https://nexora-7cs9.onrender.com/)
- **GitHub Repository:** [https://github.com/neel92654/bob-ai-hackathon-Stack_Trace](https://github.com/neel92654/bob-ai-hackathon-Stack_Trace)
- **Demo Walkthrough Video:** See [`demo/demo-video-link.txt`](../demo/demo-video-link.txt)
- **Application Screenshots:** See [`demo/screenshots/`](../demo/screenshots/)

---

## 📊 Slide Deck Structure (8 Slides)

- **Slide 1: Title & Overview** — *Nexora: Operational Risk & Supply Intelligence Platform* (IBM Bob AI Hackathon 2026, Problem Statement S2, Team Stack_Trace, Live & GitHub links).
- **Slide 2: The Problem** — Fab bottleneck congestion, queue back-pressure, single-point-of-failure (SPoF) supplier exposure, and lack of simulation tools.
- **Slide 3: Why Existing Approaches Fall Short** — Siloed MES/ERP tools, black-box opaque metrics, reactive post-mortems, and zero pre-emptive simulation.
- **Slide 4: The Nexora Solution** — End-to-end explainable intelligence answering *Where*, *How Severe*, *What Impact*, *Which Suppliers*, and *What Action*.
- **Slide 5: Technical Architecture** — React 18 frontend + Python Flask REST API + SQLite + Interpretable `RandomForestRegressor` ML ($R^2 = 0.954$) + IBM Bob MCP over STDIO.
- **Slide 6: Fab Bottleneck & SPoF Intelligence** — Live capacity utilization progress meters, 10-stage process flow starvation mapping, and 5-factor explainable supplier risk scoring.
- **Slide 7: What-If Disruption Simulator** — Proactive discrete-event simulation of supplier embargoes and equipment outages with Before vs. After metric diffs and financial SLA risk.
- **Slide 8: IBM Bob Integration & Impact** — Grounded decision assistant reasoning, prescriptive condition-driven mitigations, 52/52 tests passing, business ROI, and roadmap.

---

*For the complete slide text, layout recommendations, formulas, and speaker scripts, see [`slides.md`](slides.md).*
