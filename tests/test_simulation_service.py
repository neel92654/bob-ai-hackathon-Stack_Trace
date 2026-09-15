"""
Nexora — What-If Disruption Simulation Service Tests
"""

import pytest
from src.backend.services.simulation_service import simulate_disruption

def test_simulate_supplier_disruption():
    params = {
        "supplier_id": "SUP-002",
        "duration_days": 14
    }
    res = simulate_disruption("SUPPLIER_DISRUPTION", params)
    assert res["scenario_type"] == "SUPPLIER_DISRUPTION"
    assert res["simulated"]["supplier_risk_score"] >= res["baseline"]["supplier_risk_score"]
    assert res["delta"]["delay_increase_hours"] > 0
    assert len(res["recommended_actions"]) >= 2

def test_simulate_equipment_failure():
    params = {
        "tool_id": "CVD-03",
        "failure_duration_hours": 24
    }
    res = simulate_disruption("EQUIPMENT_FAILURE", params)
    assert res["scenario_type"] == "EQUIPMENT_FAILURE"
    assert res["simulated"]["risk_level"] == "CRITICAL"
    assert res["delta"]["delay_increase_hours"] > 0
    assert len(res["recommended_actions"]) >= 2

def test_simulate_capacity_reduction():
    params = {
        "tool_id": "LITH-01",
        "capacity_reduction_pct": 30,
        "duration_days": 7
    }
    res = simulate_disruption("CAPACITY_REDUCTION", params)
    assert res["scenario_type"] == "CAPACITY_REDUCTION"
    assert res["simulated"]["utilization_pct"] > res["baseline"]["utilization_pct"]

def test_simulate_demand_increase():
    params = {
        "demand_increase_pct": 25,
        "duration_weeks": 4
    }
    res = simulate_disruption("DEMAND_INCREASE", params)
    assert res["scenario_type"] == "DEMAND_INCREASE"
    assert res["simulated"]["critical_bottlenecks_count"] >= res["baseline"]["critical_bottlenecks_count"]

def test_simulate_invalid_scenario_raises():
    with pytest.raises(ValueError):
        simulate_disruption("UNKNOWN_SCENARIO_XYZ", {})
