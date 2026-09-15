# Source Code Structure: Nexora

This directory contains the complete source code for **Nexora — Operational Risk & Supply Intelligence Platform**.

## Architecture & Layout

```
src/
├── backend/                  # Python Flask REST API & Analytics Layer
│   ├── app.py                # Main Flask application entry point & CORS configuration
│   ├── config/
│   │   └── settings.py       # Configurable risk thresholds (LOW, MED, HIGH, CRIT) & weights
│   ├── models/
│   │   ├── database.py       # SQLite connection manager & query helpers
│   │   └── models.py
│   ├── routes/               # Flask REST Blueprints
│   │   ├── dashboard_routes.py      # GET /api/dashboard/summary
│   │   ├── bottleneck_routes.py     # GET /api/bottlenecks, GET /api/bottlenecks/<id>
│   │   ├── supplier_routes.py       # GET /api/suppliers, GET /api/suppliers/geopolitical
│   │   ├── production_routes.py     # GET /api/production/lots
│   │   ├── simulation_routes.py     # POST /api/simulation/run
│   │   ├── recommendation_routes.py # GET /api/recommendations
│   │   └── assistant_routes.py      # POST /api/assistant/query
│   ├── services/             # Core Analytics & Intelligence Services
│   │   ├── bottleneck_service.py    # Utilization & downstream process starvation
│   │   ├── supplier_risk_service.py # 5-factor weighted scoring & SPoF detection
│   │   ├── delivery_prediction_service.py # Lot impact & urgency ranking
│   │   ├── simulation_service.py    # 4-scenario What-If disruption engine
│   │   ├── recommendation_service.py # Condition-driven mitigation synthesizer
│   │   └── assistant_service.py     # Grounded decision-support reasoning
│   ├── ml/                   # Machine Learning Pipeline
│   │   ├── train_delivery_model.py  # RandomForestRegressor training (R² = 0.954)
│   │   ├── predict_delivery.py      # ML inference with deterministic physics fallback
│   │   ├── delivery_model.joblib    # Serialized model artifact
│   │   └── model_metrics.json       # Evaluated metrics (MAE, RMSE, R²)
│   ├── utils/
│   │   ├── calculations.py   # Pure, testable mathematical scoring functions
│   │   └── validators.py     # Input schema validation
│   └── requirements.txt      # Python dependencies manifest
│
├── frontend/                 # React 18 + Vite Industrial User Interface
│   ├── package.json          # Node dependencies (React, Lucide, Vite)
│   ├── vite.config.js        # Vite build & backend API proxy configuration
│   ├── index.html            # Web entry point with typography & meta tags
│   └── src/
│       ├── main.jsx          # React DOM initialization
│       ├── App.jsx           # Root layout & tab router
│       ├── index.css         # Modern industrial CSS design system
│       ├── components/       # Reusable UI components
│       │   ├── Navbar.jsx            # Header navigation & system pulse dot
│       │   ├── MetricCard.jsx        # Executive KPI cards
│       │   ├── RiskBadge.jsx         # Severity color badges
│       │   ├── ProcessFlow.jsx       # 10-stage fab process flow visualizer
│       │   ├── AlertPanel.jsx        # Real-time alert list
│       │   └── ExplainabilityModal.jsx # Factor breakdown audit modal
│       ├── pages/            # 7 Core Views
│       │   ├── Dashboard.jsx         # Executive overview
│       │   ├── Bottlenecks.jsx       # Fab equipment queue analysis
│       │   ├── SupplyChain.jsx       # Supplier risk, SPoF & geopolitical map
│       │   ├── ProductionLots.jsx    # Production lots & ML delay tracking
│       │   ├── WhatIfSimulator.jsx   # Interactive 4-scenario disruption engine
│       │   ├── Recommendations.jsx   # Prioritized mitigation action cards
│       │   └── DecisionAssistant.jsx # Grounded natural-language assistant
│       └── services/
│           └── api.js        # Centralized REST API client
│
├── data/                     # Synthetic Demonstration CSV Datasets (Seed: 42)
│   ├── process_routes.csv    # 10 sequential fab manufacturing stages
│   ├── equipment.csv         # 28 fab tools with capacity & WIP queues
│   ├── suppliers.csv         # 22 chemical/material suppliers with dependency %
│   ├── production_lots.csv   # 200 active wafer lots with customer tiers
│   ├── historical_delays.csv # 650 historical cycle records for ML training
│   └── disruptions.csv       # Active and recent disruption logs
│
└── .env.example              # Environment variables template
```
