"""
Nexora — Delivery Delay Prediction ML Model Tests
"""

import pytest
from src.backend.ml.predict_delivery import predict_delay_hours, load_model
from src.backend.services.delivery_prediction_service import get_production_lots_impact

def test_ml_model_loaded():
    model, metadata = load_model()
    assert model is not None
    assert metadata is not None
    assert "metrics" in metadata
    assert metadata["metrics"]["r2_score"] >= 0.85

def test_delivery_delay_prediction_ml():
    features = {
        "tool_nominal_capacity": 40,
        "wip_queue_size": 48,
        "tool_utilization_pct": 120.0,
        "downstream_queue_size": 35,
        "wafer_quantity": 50,
        "lot_priority_num": 3,
        "remaining_stages": 5,
        "nominal_cycle_time_hr": 6.0,
        "chamber_health": 85,
        "has_active_disruption": 0
    }
    res = predict_delay_hours(features)
    assert res["predicted_delay_hours"] >= 0.0
    assert res["method"] in ("MACHINE_LEARNING", "DETERMINISTIC_FALLBACK")
    assert len(res["feature_contributions"]) > 0

def test_delivery_delay_prediction_disruption_impact():
    # Disruption should increase predicted delay
    base = predict_delay_hours({
        "tool_nominal_capacity": 40,
        "wip_queue_size": 40,
        "tool_utilization_pct": 100.0,
        "downstream_queue_size": 20,
        "wafer_quantity": 50,
        "lot_priority_num": 2,
        "remaining_stages": 4,
        "nominal_cycle_time_hr": 5.0,
        "chamber_health": 90,
        "has_active_disruption": 0
    })
    disrupted = predict_delay_hours({
        "tool_nominal_capacity": 40,
        "wip_queue_size": 55,
        "tool_utilization_pct": 137.5,
        "downstream_queue_size": 20,
        "wafer_quantity": 50,
        "lot_priority_num": 2,
        "remaining_stages": 4,
        "nominal_cycle_time_hr": 5.0,
        "chamber_health": 70,
        "has_active_disruption": 1
    })
    assert disrupted["predicted_delay_hours"] > base["predicted_delay_hours"]

def test_get_production_lots_impact_service():
    res = get_production_lots_impact()
    assert "summary" in res
    assert "lots" in res
    assert res["summary"]["total_lots"] >= 150
    assert res["summary"]["average_predicted_delay_hours"] >= 0.0
