"""
Nexora — Automated MCP Server Tool Discovery & Execution Tests
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

import pytest
import asyncio
import os
import sys
import importlib.util

# Ensure repository root is on path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)
MCP_SERVER_DIR = os.path.join(REPO_ROOT, "mcp-server")
sys.path.insert(0, MCP_SERVER_DIR)

# Dynamically import mcp-server/server.py
server_path = os.path.join(MCP_SERVER_DIR, "server.py")
spec = importlib.util.spec_from_file_location("nexora_mcp_server", server_path)
nexora_mcp = importlib.util.module_from_spec(spec)
sys.modules["nexora_mcp_server"] = nexora_mcp
spec.loader.exec_module(nexora_mcp)

mcp = nexora_mcp.mcp
get_fab_bottlenecks = nexora_mcp.get_fab_bottlenecks
get_bottleneck_details = nexora_mcp.get_bottleneck_details
get_supplier_risk = nexora_mcp.get_supplier_risk
get_supplier_details = nexora_mcp.get_supplier_details
get_production_impact = nexora_mcp.get_production_impact
run_disruption_simulation = nexora_mcp.run_disruption_simulation
get_recommendations = nexora_mcp.get_recommendations
get_executive_summary = nexora_mcp.get_executive_summary

def test_mcp_tool_discovery():
    """Verify that all 8 required MCP tools are properly discovered by the MCP server."""
    tools = asyncio.run(mcp.list_tools())
    tool_names = [t.name for t in tools]
    
    expected_tools = [
        "get_fab_bottlenecks",
        "get_bottleneck_details",
        "get_supplier_risk",
        "get_supplier_details",
        "get_production_impact",
        "run_disruption_simulation",
        "get_recommendations",
        "get_executive_summary"
    ]
    
    for et in expected_tools:
        assert et in tool_names, f"MCP tool '{et}' not registered on server."
    assert len(tool_names) == 8

def test_mcp_get_fab_bottlenecks_all():
    """Test get_fab_bottlenecks tool with no filter."""
    res = get_fab_bottlenecks()
    assert res["status"] == "success"
    assert res["count"] >= 20
    assert any(b["tool_id"] == "CVD-03" for b in res["bottlenecks"])

def test_mcp_get_fab_bottlenecks_filter_critical():
    """Test get_fab_bottlenecks tool filtering by CRITICAL severity."""
    res = get_fab_bottlenecks(severity="CRITICAL")
    assert res["status"] == "success"
    assert all(b["risk_level"] == "CRITICAL" for b in res["bottlenecks"])
    assert any(b["tool_id"] == "CVD-03" for b in res["bottlenecks"])

def test_mcp_get_bottleneck_details_valid():
    """Test get_bottleneck_details for CVD-03."""
    res = get_bottleneck_details("CVD-03")
    assert res["status"] == "success"
    tool = res["tool"]
    assert tool["tool_id"] == "CVD-03"
    assert tool["utilization_pct"] > 120.0
    assert tool["risk_level"] == "CRITICAL"
    assert len(tool["assigned_lots_summary"]) > 0
    assert len(tool["downstream_processes_affected"]) > 0

def test_mcp_get_bottleneck_details_invalid():
    """Test get_bottleneck_details returns clean error for unknown tool."""
    res = get_bottleneck_details("INVALID_TOOL_99")
    assert res["status"] == "error"
    assert "not found" in res["message"]

def test_mcp_get_supplier_risk():
    """Test get_supplier_risk tool."""
    res = get_supplier_risk()
    assert res["status"] == "success"
    assert res["total_suppliers"] >= 20
    assert res["spof_count"] >= 2
    assert any(s["supplier_id"] == "SUP-002" for s in res["suppliers"])
    assert len(res["top_geopolitical_exposures"]) > 0

def test_mcp_get_supplier_details_valid():
    """Test get_supplier_details for SPoF supplier SUP-002."""
    res = get_supplier_details("SUP-002")
    assert res["status"] == "success"
    supp = res["supplier"]
    assert supp["supplier_id"] == "SUP-002"
    assert supp["is_single_point_of_failure"] is True
    assert supp["risk_level"] == "CRITICAL"
    assert "factor_breakdown" in supp

def test_mcp_get_supplier_details_invalid():
    """Test get_supplier_details returns clean error for unknown supplier."""
    res = get_supplier_details("SUP_UNKNOWN_99")
    assert res["status"] == "error"
    assert "not found" in res["message"]

def test_mcp_get_production_impact_summary():
    """Test get_production_impact with summary output."""
    res = get_production_impact()
    assert res["status"] == "success"
    assert "summary" in res
    assert res["summary"]["total_lots"] >= 150
    assert len(res["top_urgent_lots"]) > 0

def test_mcp_get_production_impact_single_lot():
    """Test get_production_impact for a specific lot ID."""
    res = get_production_impact(lot_id="LOT-0001")
    assert res["status"] == "success"
    assert res["lot"]["lot_id"] == "LOT-0001"
    assert res["lot"]["predicted_delay_hours"] >= 0.0

def test_mcp_run_disruption_simulation_supplier():
    """Test run_disruption_simulation for supplier disruption."""
    res = run_disruption_simulation(
        scenario_type="SUPPLIER_DISRUPTION",
        target_id="SUP-002",
        duration_days=14
    )
    assert res["status"] == "success"
    sim = res["simulation"]
    assert sim["scenario_type"] == "SUPPLIER_DISRUPTION"
    assert sim["simulated"]["supplier_risk_score"] >= sim["baseline"]["supplier_risk_score"]
    assert sim["delta"]["delay_increase_hours"] > 0
    assert len(sim["recommended_actions"]) >= 2

def test_mcp_run_disruption_simulation_equipment():
    """Test run_disruption_simulation for equipment failure."""
    res = run_disruption_simulation(
        scenario_type="EQUIPMENT_FAILURE",
        target_id="CVD-03",
        failure_duration_hours=24
    )
    assert res["status"] == "success"
    sim = res["simulation"]
    assert sim["scenario_type"] == "EQUIPMENT_FAILURE"
    assert sim["simulated"]["risk_level"] == "CRITICAL"
    assert len(sim["recommended_actions"]) >= 2

def test_mcp_run_disruption_simulation_invalid():
    """Test run_disruption_simulation handles unknown scenario gracefully."""
    res = run_disruption_simulation(scenario_type="INVALID_SCENARIO_ABC")
    assert res["status"] == "error"
    assert "Unknown scenario_type" in res["message"]

def test_mcp_get_recommendations():
    """Test get_recommendations tool."""
    res = get_recommendations()
    assert res["status"] == "success"
    assert res["total_recommendations"] > 0
    assert res["critical_count"] > 0
    assert len(res["recommendations"]) > 0

def test_mcp_get_executive_summary():
    """Test get_executive_summary tool."""
    res = get_executive_summary()
    assert res["status"] == "success"
    assert "kpi_summary" in res
    assert res["kpi_summary"]["overall_operational_risk_score"] > 0
    assert res["kpi_summary"]["critical_bottlenecks_count"] > 0
    assert len(res["critical_alerts"]) > 0
    assert len(res["top_mitigations"]) > 0
