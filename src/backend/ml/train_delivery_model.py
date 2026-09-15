"""
Nexora — Delivery Delay Prediction Model Training Pipeline
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)

Trains an interpretable RandomForestRegressor model on historical fab cycle delay data,
evaluates genuine metrics (MAE, RMSE, R²), extracts feature importances, and saves the pipeline artifact.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DATA_PATH = os.path.join(BASE_DIR, "src", "data", "historical_delays.csv")
MODEL_DIR = os.path.join(BASE_DIR, "src", "backend", "ml")
MODEL_PATH = os.path.join(MODEL_DIR, "delivery_model.joblib")
METRICS_PATH = os.path.join(MODEL_DIR, "model_metrics.json")

FEATURE_COLS = [
    "tool_nominal_capacity",
    "wip_queue_size",
    "tool_utilization_pct",
    "downstream_queue_size",
    "wafer_quantity",
    "lot_priority_num",
    "remaining_stages",
    "nominal_cycle_time_hr",
    "chamber_health",
    "has_active_disruption"
]

TARGET_COL = "actual_delay_hours"

def train_model():
    print(f"Loading historical delay training dataset from: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH)
    
    X = df[FEATURE_COLS]
    y = df[TARGET_COL]
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42
    )
    
    print(f"Training set: {X_train.shape[0]} samples | Test set: {X_test.shape[0]} samples")
    
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=12,
        min_samples_split=4,
        min_samples_leaf=2,
        random_state=42
    )
    
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    mae = float(mean_absolute_error(y_test, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = float(r2_score(y_test, y_pred))
    
    feature_importances = {
        col: float(imp) for col, imp in zip(FEATURE_COLS, model.feature_importances_)
    }
    sorted_importances = dict(sorted(feature_importances.items(), key=lambda item: item[1], reverse=True))
    
    print("=" * 60)
    print("Model Evaluation Metrics:")
    print(f"  • Mean Absolute Error (MAE) : {mae:.3f} hours")
    print(f"  • Root Mean Squared Error (RMSE): {rmse:.3f} hours")
    print(f"  • R² Score                  : {r2:.4f}")
    print("Top Feature Importances:")
    for k, v in list(sorted_importances.items())[:5]:
        print(f"  - {k}: {v*100:.2f}%")
    print("=" * 60)
    
    metadata = {
        "model_type": "RandomForestRegressor",
        "n_estimators": 100,
        "features": FEATURE_COLS,
        "target": TARGET_COL,
        "metrics": {
            "mae_hours": round(mae, 3),
            "rmse_hours": round(rmse, 3),
            "r2_score": round(r2, 4),
            "test_samples": len(y_test),
            "train_samples": len(y_train)
        },
        "feature_importances": sorted_importances,
        "trained_timestamp": pd.Timestamp.now().isoformat()
    }
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump({"model": model, "metadata": metadata}, MODEL_PATH)
    print(f"Saved model artifact to: {MODEL_PATH}")
    
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved model metrics to: {METRICS_PATH}")
    
    return metadata

if __name__ == "__main__":
    train_model()
