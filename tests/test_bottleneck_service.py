"""
Nexora — Bottleneck Calculations & Intelligence Service Tests
"""

import pytest
from src.backend.utils.calculations import calculate_bottleneck_metrics
from src.backend.services.bottleneck_service import get_all_bottlenecks, get_bottleneck_by_id

def test_bottleneck_calculation_low_risk():
    res = calculate_bottleneck_metrics(nominal_capacity=50, current_wip=30, tool_id="TEST-01")
    assert res["utilization_pct"] == 60.0
    assert res["risk_level"] == "LOW"
    assert res["queue_pressure"] == 0
    assert "operating within normal bounds" in res["explanation"]

def test_bottleneck_calculation_critical_risk():
    res = calculate_bottleneck_metrics(nominal_capacity=30, current_wip=46, tool_id="CVD-03", affected_lot_count=18)
    assert res["utilization_pct"] == 153.3
    assert res["risk_level"] == "CRITICAL"
    assert res["queue_pressure"] == 16
    assert "CVD-03 is classified as CRITICAL" in res["explanation"]
    assert "18 active downstream lots" in res["explanation"]

def test_bottleneck_classification_boundaries():
    # 79% -> LOW
    assert calculate_bottleneck_metrics(100, 79)["risk_level"] == "LOW"
    # 85% -> MEDIUM
    assert calculate_bottleneck_metrics(100, 85)["risk_level"] == "MEDIUM"
    # 105% -> HIGH
    assert calculate_bottleneck_metrics(100, 105)["risk_level"] == "HIGH"
    # 125% -> CRITICAL
    assert calculate_bottleneck_metrics(100, 125)["risk_level"] == "CRITICAL"

def test_get_all_bottlenecks_service():
    bottlenecks = get_all_bottlenecks()
    assert len(bottlenecks) >= 20
    assert any(b["tool_id"] == "CVD-03" for b in bottlenecks)
    # Check that sorting puts critical tools first
    assert bottlenecks[0]["risk_level"] in ("CRITICAL", "HIGH")

def test_get_bottleneck_by_id():
    tool = get_bottleneck_by_id("CVD-03")
    assert tool is not None
    assert tool["tool_id"] == "CVD-03"
    assert "assigned_lots" in tool
    assert "process_roadmap" in tool
    assert len(tool["process_roadmap"]) == 10

def test_get_bottleneck_by_id_not_found():
    tool = get_bottleneck_by_id("NONEXISTENT-TOOL-99")
    assert tool is None
