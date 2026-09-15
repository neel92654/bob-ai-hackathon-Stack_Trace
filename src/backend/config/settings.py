"""
Nexora — Configuration & Threshold Settings
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DB_PATH = os.path.join(BASE_DIR, "src", "backend", "database", "nexora.db")

# Bottleneck Utilization Thresholds (Configurable)
BOTTLENECK_THRESHOLDS = {
    "LOW": 80.0,       # < 80%
    "MEDIUM": 100.0,   # 80% to < 100%
    "HIGH": 120.0,     # 100% to < 120%
    "CRITICAL": 120.0  # >= 120%
}

# Explainable Supplier Risk Scoring Weights (Sum to 1.0)
SUPPLIER_RISK_WEIGHTS = {
    "dependency": 0.30,       # Market / dependency share
    "lead_time": 0.25,        # Lead time relative to 60-day baseline
    "criticality": 0.20,      # Material criticality (CRITICAL=100, HIGH=75, MED=50, LOW=25)
    "geographic_risk": 0.15,  # Geopolitical factor (1.0 to 2.0 scaled to 0-100)
    "alternate_avail": 0.10   # Alternate supplier penalty (None = 100, Partial = 60, Dual = 10)
}

# Supplier Risk Level Classification
SUPPLIER_RISK_THRESHOLDS = {
    "LOW": 25.0,       # 0 to 24
    "MEDIUM": 50.0,    # 25 to 49
    "HIGH": 75.0,      # 50 to 74
    "CRITICAL": 100.0  # 75 to 100
}

# Single Point of Failure (SPoF) Thresholds
SPOF_CONDITIONS = {
    "min_dependency_pct": 75,
    "require_no_full_alternate": True,
    "critical_materials": ["Gallium", "Neon Gas", "Palladium", "TMA", "EUV Photoresist"]
}

APP_PORT = int(os.environ.get("APP_PORT", 5001))
DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")
