"""
Nexora — Supplier Risk, SPoF Detection & Geopolitical Tests
"""

import pytest
from src.backend.utils.calculations import calculate_supplier_risk_score, calculate_country_concentration
from src.backend.services.supplier_risk_service import (
    get_all_suppliers_risk,
    get_supplier_by_id,
    get_geopolitical_summary
)

def test_supplier_risk_score_spof_critical():
    supplier_data = {
        "name": "Global Gallium Refining Ltd.",
        "material": "High-Purity Gallium",
        "dependency_pct": 91,
        "lead_time_days": 45,
        "criticality": "CRITICAL",
        "alternate_supplier": "None",
        "alternate_capacity_pct": 0,
        "geo_risk_factor": 1.8,
        "single_point_of_failure": 1
    }
    score_res = calculate_supplier_risk_score(supplier_data)
    assert score_res["supplier_risk_score"] >= 75.0
    assert score_res["risk_level"] == "CRITICAL"
    assert score_res["is_single_point_of_failure"] is True
    assert any("High market dependency" in r for r in score_res["risk_reasons"])
    assert any("No full secondary supplier" in r for r in score_res["risk_reasons"])

def test_supplier_risk_score_low_risk():
    supplier_data = {
        "name": "Local Solvent Corp.",
        "material": "Standard Solvent",
        "dependency_pct": 20,
        "lead_time_days": 10,
        "criticality": "LOW",
        "alternate_supplier": "Alt Solvent Inc.",
        "alternate_capacity_pct": 80,
        "geo_risk_factor": 1.0,
        "single_point_of_failure": 0
    }
    score_res = calculate_supplier_risk_score(supplier_data)
    assert score_res["supplier_risk_score"] < 25.0
    assert score_res["risk_level"] == "LOW"
    assert score_res["is_single_point_of_failure"] is False

def test_get_all_suppliers_service():
    suppliers = get_all_suppliers_risk()
    assert len(suppliers) >= 20
    assert any(s["supplier_id"] == "SUP-002" for s in suppliers)
    # Check that SPoF suppliers are sorted to the front
    assert suppliers[0]["is_single_point_of_failure"] is True

def test_get_supplier_by_id():
    supp = get_supplier_by_id("SUP-002")
    assert supp is not None
    assert supp["supplier_id"] == "SUP-002"
    assert "affected_lots" in supp
    assert supp["is_single_point_of_failure"] is True

def test_country_concentration_calculation():
    geo = get_geopolitical_summary()
    assert len(geo) > 0
    # Check required fields
    for item in geo:
        assert "country" in item
        assert "supplier_count" in item
        assert "average_dependency_pct" in item
        assert "concentration_level" in item
