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
    # Verify supplier-specific recommendation grounding
    assert "mitigation_recommendation" in res
    assert "Gallium" in res["mitigation_recommendation"]["action"] or "SUP-002" in res["mitigation_recommendation"]["action"]
    assert "operational_impact_summary" in res
    assert "Gallium" in res["operational_impact_summary"]

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
    # Verify equipment-specific recommendation grounding
    assert "mitigation_recommendation" in res
    assert "CVD-03" in res["mitigation_recommendation"]["action"] or "alternate" in res["mitigation_recommendation"]["action"].lower()
    assert "operational_impact_summary" in res
    assert "CVD-03" in res["operational_impact_summary"]

def test_simulate_capacity_reduction():
    params = {
        "tool_id": "LITH-01",
        "capacity_reduction_pct": 30,
        "duration_days": 7
    }
    res = simulate_disruption("CAPACITY_REDUCTION", params)
    assert res["scenario_type"] == "CAPACITY_REDUCTION"
    assert res["simulated"]["utilization_pct"] > res["baseline"]["utilization_pct"]
    # Verify capacity-specific recommendation grounding
    assert "mitigation_recommendation" in res
    assert "LITH-01" in res["mitigation_recommendation"]["action"] or "chamber" in res["mitigation_recommendation"]["action"].lower()
    assert "30%" in res["mitigation_recommendation"]["detail"]

def test_simulate_demand_increase():
    params = {
        "demand_increase_pct": 25,
        "duration_weeks": 4
    }
    res = simulate_disruption("DEMAND_INCREASE", params)
    assert res["scenario_type"] == "DEMAND_INCREASE"
    assert res["simulated"]["critical_bottlenecks_count"] >= res["baseline"]["critical_bottlenecks_count"]
    # Verify demand-specific recommendation grounding
    assert "mitigation_recommendation" in res
    assert "25%" in res["mitigation_recommendation"]["action"] or "volume" in res["mitigation_recommendation"]["action"].lower()
    assert "25%" in res["mitigation_recommendation"]["detail"]

def test_simulation_recommendations_are_distinct_and_dynamic():
    """Verify that all four scenario categories produce distinct, non-identical recommendations."""
    res_sup = simulate_disruption("SUPPLIER_DISRUPTION", {"supplier_id": "SUP-002", "duration_days": 14})
    res_eq = simulate_disruption("EQUIPMENT_FAILURE", {"tool_id": "CVD-03", "failure_duration_hours": 24})
    res_cap = simulate_disruption("CAPACITY_REDUCTION", {"tool_id": "LITH-01", "capacity_reduction_pct": 30, "duration_days": 7})
    res_dem = simulate_disruption("DEMAND_INCREASE", {"demand_increase_pct": 25, "duration_weeks": 4})

    actions = [
        res_sup["mitigation_recommendation"]["action"],
        res_eq["mitigation_recommendation"]["action"],
        res_cap["mitigation_recommendation"]["action"],
        res_dem["mitigation_recommendation"]["action"]
    ]
    # All 4 primary actions must be unique
    assert len(set(actions)) == 4, f"Recommendations must be distinct across scenarios: {actions}"

    # Also verify recommendations adapt to different entity inputs
    res_sup4 = simulate_disruption("SUPPLIER_DISRUPTION", {"supplier_id": "SUP-004", "duration_days": 10})
    assert "Neon" in res_sup4["mitigation_recommendation"]["action"] or "SUP-004" in res_sup4["mitigation_recommendation"]["action"]
    assert res_sup4["mitigation_recommendation"]["action"] != res_sup["mitigation_recommendation"]["action"]

def test_simulate_invalid_scenario_raises():
    with pytest.raises(ValueError):
        simulate_disruption("UNKNOWN_SCENARIO_XYZ", {})
