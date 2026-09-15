"""
Nexora — Model Context Protocol (MCP) Server
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)

Exposes Nexora's operational intelligence, fab bottleneck analytics, supplier risk scoring,
ML delivery delay predictions, and What-If disruption simulations as standard MCP tools for IBM Bob.
"""

import sys
import os
from typing import Optional, Dict, Any, List

# Ensure repository root is on Python module search path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from mcp.server.mcpserver import MCPServer

# Import existing Nexora analytics and decision services (Zero duplication)
from src.backend.services.bottleneck_service import get_all_bottlenecks, get_bottleneck_by_id
from src.backend.services.supplier_risk_service import (
    get_all_suppliers_risk,
    get_supplier_by_id,
    get_geopolitical_summary
)
from src.backend.services.delivery_prediction_service import (
    get_production_lots_impact,
    get_lot_by_id
)
from src.backend.services.simulation_service import simulate_disruption
from src.backend.services.recommendation_service import generate_recommendations
from src.backend.models.database import query_db

# Initialize Nexora MCP Server
mcp = MCPServer(
    name="nexora-mcp-server",
    title="Nexora Operational Risk & Supply Intelligence MCP Server",
    version="1.0.0",
    description="MCP Tool Provider connecting IBM Bob to Nexora's fab bottleneck intelligence, SPoF supplier scoring, and What-If disruption simulation engine."
)

@mcp.tool(
    name="get_fab_bottlenecks",
    description=(
        "Retrieves Nexora's current semiconductor fabrication bottlenecks across all equipment tools. "
        "Use this when IBM Bob is asked which fab tools or process stages are currently constraining production. "
        "Returns utilization (WIP / Rated Capacity), current WIP, rated capacity, queue overload, severity rating (LOW, MEDIUM, HIGH, CRITICAL), "
        "plain-English explainable diagnosis, affected production lots count, and ML-predicted delay in hours. "
        "Supports optional filtering by severity (e.g., 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW')."
    )
)
def get_fab_bottlenecks(severity: Optional[str] = None) -> Dict[str, Any]:
    try:
        bottlenecks = get_all_bottlenecks()
        if severity:
            norm_sev = severity.strip().upper()
            bottlenecks = [b for b in bottlenecks if b.get("risk_level", "").upper() == norm_sev]
        
        return {
            "status": "success",
            "count": len(bottlenecks),
            "filter_applied": {"severity": severity} if severity else "none",
            "bottlenecks": [
                {
                    "tool_id": b["tool_id"],
                    "name": b["name"],
                    "process_id": b["process_id"],
                    "process_name": b["process_name"],
                    "utilization_pct": b["utilization_pct"],
                    "current_wip": b["current_wip"],
                    "nominal_capacity": b["nominal_capacity"],
                    "queue_pressure": b["queue_pressure"],
                    "risk_level": b["risk_level"],
                    "risk_score": b["risk_score"],
                    "explanation": b["explanation"],
                    "affected_lot_count": b["affected_lot_count"],
                    "high_priority_lot_count": b["high_priority_lot_count"],
                    "predicted_delay_hours": b["predicted_delay_hours"],
                    "chamber_health": b["chamber_health"],
                    "maintenance_due_hours": b["maintenance_due_hours"]
                }
                for b in bottlenecks
            ]
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve fab bottlenecks: {str(e)}"}

@mcp.tool(
    name="get_bottleneck_details",
    description=(
        "Retrieves detailed bottleneck diagnostics, process roadmap dependencies, and assigned wafer lots for a specific tool ID (e.g., 'CVD-03', 'LITH-01'). "
        "Use this when IBM Bob needs deep-dive root cause analysis for a specific equipment item, including chamber health status, MTBF, "
        "downstream starvation paths across the 10-stage process sequence, and all individual queued production lots."
    )
)
def get_bottleneck_details(tool_id: str) -> Dict[str, Any]:
    try:
        if not tool_id or not isinstance(tool_id, str):
            return {"status": "error", "message": "A valid tool_id string is required (e.g. 'CVD-03')."}

        tool = get_bottleneck_by_id(tool_id.strip().upper())
        if not tool:
            return {"status": "error", "message": f"Equipment item with ID '{tool_id}' was not found in Nexora telemetry."}

        return {
            "status": "success",
            "tool": {
                "tool_id": tool["tool_id"],
                "name": tool["name"],
                "process_id": tool["process_id"],
                "process_name": tool["process_name"],
                "step_seq": tool["step_seq"],
                "nominal_capacity": tool["nominal_capacity"],
                "current_wip": tool["current_wip"],
                "utilization_pct": tool["utilization_pct"],
                "queue_pressure": tool["queue_pressure"],
                "risk_level": tool["risk_level"],
                "risk_score": tool["risk_score"],
                "explanation": tool["explanation"],
                "chamber_health": tool["chamber_health"],
                "maintenance_due_hours": tool["maintenance_due_hours"],
                "mtbf_hours": tool["mtbf_hours"],
                "affected_lot_count": tool["affected_lot_count"],
                "high_priority_lot_count": tool["high_priority_lot_count"],
                "predicted_delay_hours": tool["predicted_delay_hours"],
                "prediction_confidence": tool["prediction_confidence"],
                "downstream_processes_affected": tool["downstream_processes"],
                "assigned_lots_summary": [
                    {
                        "lot_id": l["lot_id"],
                        "product_family": l["product_family"],
                        "customer_tier": l["customer_tier"],
                        "wafer_quantity": l["wafer_quantity"],
                        "priority": l["priority"],
                        "due_date": l["due_date"]
                    }
                    for l in tool.get("assigned_lots", [])[:10]
                ]
            }
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve bottleneck details for {tool_id}: {str(e)}"}

@mcp.tool(
    name="get_supplier_risk",
    description=(
        "Retrieves the explainable supplier risk ranking across all raw material and chemical suppliers. "
        "Use this when IBM Bob is asked about supply chain vulnerabilities, Single-Point-of-Failure (SPoF) risks, supplier lead times, or geopolitical concentration. "
        "Returns explainable 5-factor weighted scores (0–100), SPoF flags, material names, origin countries, dependency shares %, and lead times."
    )
)
def get_supplier_risk(min_risk_level: Optional[str] = None) -> Dict[str, Any]:
    try:
        suppliers = get_all_suppliers_risk()
        if min_risk_level:
            norm_lvl = min_risk_level.strip().upper()
            level_hierarchy = {"CRITICAL": ["CRITICAL"], "HIGH": ["CRITICAL", "HIGH"], "MEDIUM": ["CRITICAL", "HIGH", "MEDIUM"], "LOW": ["CRITICAL", "HIGH", "MEDIUM", "LOW"]}
            allowed = level_hierarchy.get(norm_lvl, [norm_lvl])
            suppliers = [s for s in suppliers if s.get("risk_level", "").upper() in allowed]

        geo = get_geopolitical_summary()
        spof_count = sum(1 for s in suppliers if s.get("is_single_point_of_failure"))

        return {
            "status": "success",
            "total_suppliers": len(suppliers),
            "spof_count": spof_count,
            "suppliers": [
                {
                    "supplier_id": s["supplier_id"],
                    "name": s["name"],
                    "material": s["material"],
                    "country": s["country"],
                    "dependency_pct": s["dependency_pct"],
                    "lead_time_days": s["lead_time_days"],
                    "criticality": s["criticality"],
                    "is_single_point_of_failure": s["is_single_point_of_failure"],
                    "supplier_risk_score": s["supplier_risk_score"],
                    "risk_level": s["risk_level"],
                    "risk_reasons": s["risk_reasons"],
                    "alternate_supplier": s["alternate_supplier"],
                    "alternate_capacity_pct": s["alternate_capacity_pct"]
                }
                for s in suppliers
            ],
            "top_geopolitical_exposures": [
                {
                    "country": g["country"],
                    "supplier_count": g["supplier_count"],
                    "average_dependency_pct": g["average_dependency_pct"],
                    "critical_materials": g["critical_materials"],
                    "concentration_level": g["concentration_level"]
                }
                for g in geo[:3]
            ]
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve supplier risk: {str(e)}"}

@mcp.tool(
    name="get_supplier_details",
    description=(
        "Retrieves detailed risk profiling, factor weight breakdowns, alternate supplier availability, and affected fab process stages for a specific supplier ID (e.g., 'SUP-002', 'SUP-004'). "
        "Use this when IBM Bob is asked why a specific supplier is risky, what happens if their material is delayed, or what secondary sources exist."
    )
)
def get_supplier_details(supplier_id: str) -> Dict[str, Any]:
    try:
        if not supplier_id or not isinstance(supplier_id, str):
            return {"status": "error", "message": "A valid supplier_id string is required (e.g. 'SUP-002')."}

        supp = get_supplier_by_id(supplier_id.strip().upper())
        if not supp:
            return {"status": "error", "message": f"Supplier with ID '{supplier_id}' was not found in Nexora records."}

        return {
            "status": "success",
            "supplier": {
                "supplier_id": supp["supplier_id"],
                "name": supp["name"],
                "material": supp["material"],
                "country": supp["country"],
                "lead_time_days": supp["lead_time_days"],
                "dependency_pct": supp["dependency_pct"],
                "criticality": supp["criticality"],
                "is_single_point_of_failure": supp["is_single_point_of_failure"],
                "supplier_risk_score": supp["supplier_risk_score"],
                "risk_level": supp["risk_level"],
                "factor_breakdown": supp["factor_breakdown"],
                "risk_reasons": supp["risk_reasons"],
                "explanation": supp["explanation"],
                "alternate_supplier": supp["alternate_supplier"],
                "alternate_lead_time_days": supp["alternate_lead_time_days"],
                "alternate_capacity_pct": supp["alternate_capacity_pct"],
                "affected_process_names": supp["affected_process_names"],
                "affected_lots_count": supp.get("affected_lots_count", 0),
                "affected_wafers_total": supp.get("affected_wafers_total", 0)
            }
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve supplier details for {supplier_id}: {str(e)}"}

@mcp.tool(
    name="get_production_impact",
    description=(
        "Retrieves production lot impact tracking, order valuations, and machine learning delivery delay predictions across active wafer lots. "
        "Use this when IBM Bob is asked which production lots are most delayed, which customer orders are at risk, or to look up a specific lot ID (e.g. 'LOT-0001'). "
        "Returns process stage, wafer quantity, priority, original due date, revised delivery due date, ML predicted delay hours, and order urgency ranking."
    )
)
def get_production_impact(
    lot_id: Optional[str] = None,
    priority: Optional[str] = None,
    process_id: Optional[str] = None
) -> Dict[str, Any]:
    try:
        if lot_id:
            lot = get_lot_by_id(lot_id.strip().upper())
            if not lot:
                return {"status": "error", "message": f"Production lot '{lot_id}' was not found."}
            return {"status": "success", "lot": lot}

        data = get_production_lots_impact(filter_priority=priority, filter_process=process_id)
        return {
            "status": "success",
            "summary": data["summary"],
            "total_returned": len(data["lots"]),
            "top_urgent_lots": [
                {
                    "lot_id": l["lot_id"],
                    "product_family": l["product_family"],
                    "customer_tier": l["customer_tier"],
                    "current_process_name": l["current_process_name"],
                    "assigned_tool_id": l["assigned_tool_id"],
                    "wafer_quantity": l["wafer_quantity"],
                    "priority": l["priority"],
                    "predicted_delay_hours": l["predicted_delay_hours"],
                    "original_due_date": l["original_due_date"],
                    "revised_due_date": l["revised_due_date"],
                    "urgency_score": l["urgency_score"],
                    "impact_level": l["impact_level"]
                }
                for l in data["lots"][:15]
            ]
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve production impact: {str(e)}"}

@mcp.tool(
    name="run_disruption_simulation",
    description=(
        "Executes a What-If operational disruption simulation to stress-test fab resilience and customer SLA exposure before committing line changes. "
        "Use this when IBM Bob is asked 'What happens if...', asks to simulate a multi-day supplier outage, tool breakdown, capacity drop, or demand surge. "
        "Supported scenario_types: 'SUPPLIER_DISRUPTION', 'EQUIPMENT_FAILURE', 'CAPACITY_REDUCTION', 'DEMAND_INCREASE'. "
        "Returns structured BEFORE vs. AFTER metric comparisons, changed utilization, affected lot count, delay increase, financial exposure ($), and recommended mitigations."
    )
)
def run_disruption_simulation(
    scenario_type: str,
    target_id: Optional[str] = None,
    duration_days: Optional[int] = 14,
    failure_duration_hours: Optional[int] = 24,
    capacity_reduction_pct: Optional[float] = 30.0,
    demand_increase_pct: Optional[float] = 25.0,
    duration_weeks: Optional[int] = 4
) -> Dict[str, Any]:
    try:
        if not scenario_type:
            return {"status": "error", "message": "scenario_type is required (SUPPLIER_DISRUPTION, EQUIPMENT_FAILURE, CAPACITY_REDUCTION, DEMAND_INCREASE)."}

        norm_type = scenario_type.strip().upper()
        params: Dict[str, Any] = {}

        if norm_type == "SUPPLIER_DISRUPTION":
            params = {
                "supplier_id": (target_id or "SUP-002").strip().upper(),
                "duration_days": int(duration_days or 14)
            }
        elif norm_type == "EQUIPMENT_FAILURE":
            params = {
                "tool_id": (target_id or "CVD-03").strip().upper(),
                "failure_duration_hours": int(failure_duration_hours or 24)
            }
        elif norm_type == "CAPACITY_REDUCTION":
            params = {
                "tool_id": (target_id or "LITH-01").strip().upper(),
                "capacity_reduction_pct": float(capacity_reduction_pct or 30.0),
                "duration_days": int(duration_days or 7)
            }
        elif norm_type == "DEMAND_INCREASE":
            params = {
                "demand_increase_pct": float(demand_increase_pct or 25.0),
                "duration_weeks": int(duration_weeks or 4)
            }
        else:
            return {
                "status": "error",
                "message": f"Unknown scenario_type '{scenario_type}'. Must be SUPPLIER_DISRUPTION, EQUIPMENT_FAILURE, CAPACITY_REDUCTION, or DEMAND_INCREASE."
            }

        result = simulate_disruption(norm_type, params)
        return {
            "status": "success",
            "simulation": result
        }
    except ValueError as ve:
        return {"status": "error", "message": str(ve)}
    except Exception as e:
        return {"status": "error", "message": f"Simulation execution failed: {str(e)}"}

@mcp.tool(
    name="get_recommendations",
    description=(
        "Retrieves prioritized, condition-driven operational mitigations synthesized from live fab tool bottlenecks, SPoF exposures, and active disruptions. "
        "Use this when IBM Bob is asked 'What should we do?', 'What should operations prioritize?', or needs a prescriptive response protocol. "
        "Returns prioritized actions, operational rationales, target tools/suppliers, and expected business benefits. "
        "Supports optional filtering by category ('FAB_BOTTLENECK', 'SUPPLY_CHAIN_SPOF', 'PREVENTIVE_MAINTENANCE', 'DISRUPTION_MITIGATION') and priority ('CRITICAL', 'HIGH', 'MEDIUM')."
    )
)
def get_recommendations(
    category: Optional[str] = None,
    priority: Optional[str] = None
) -> Dict[str, Any]:
    try:
        recs = generate_recommendations(category_filter=category, priority_filter=priority)
        return {
            "status": "success",
            "total_recommendations": recs["total_recommendations"],
            "critical_count": recs["critical_count"],
            "high_count": recs["high_count"],
            "recommendations": recs["recommendations"]
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to retrieve recommendations: {str(e)}"}

@mcp.tool(
    name="get_executive_summary",
    description=(
        "Retrieves a high-level executive operational summary of the entire semiconductor fabrication facility and supply chain status. "
        "Use this when IBM Bob is asked for an overall fab status, operational health check, executive briefing, or summary of all active risks. "
        "Returns overall operational risk score (0–100) & tier, active and critical bottleneck counts, SPoF supplier counts, total affected lots, average ML delay, real-time alerts, and top mitigations."
    )
)
def get_executive_summary() -> Dict[str, Any]:
    try:
        bottlenecks = get_all_bottlenecks()
        suppliers = get_all_suppliers_risk()
        lots_impact = get_production_lots_impact()
        recs = generate_recommendations()
        disruptions = query_db("SELECT * FROM disruptions WHERE status = 'ACTIVE'")

        critical_bottlenecks = [b for b in bottlenecks if b["risk_level"] == "CRITICAL"]
        high_bottlenecks = [b for b in bottlenecks if b["risk_level"] == "HIGH"]
        spof_suppliers = [s for s in suppliers if s["is_single_point_of_failure"]]
        critical_suppliers = [s for s in suppliers if s["risk_level"] == "CRITICAL"]

        bottleneck_risk_index = min(100.0, len(critical_bottlenecks) * 35.0 + len(high_bottlenecks) * 15.0)
        supplier_risk_index = min(100.0, len(spof_suppliers) * 25.0 + len(critical_suppliers) * 20.0)
        disruption_risk_index = min(100.0, len(disruptions) * 30.0)
        overall_risk_score = round(bottleneck_risk_index * 0.40 + supplier_risk_index * 0.35 + disruption_risk_index * 0.25, 1)

        if overall_risk_score >= 75:
            overall_risk_level = "CRITICAL"
        elif overall_risk_score >= 50:
            overall_risk_level = "HIGH"
        elif overall_risk_score >= 25:
            overall_risk_level = "MEDIUM"
        else:
            overall_risk_level = "LOW"

        return {
            "status": "success",
            "kpi_summary": {
                "overall_operational_risk_score": overall_risk_score,
                "overall_operational_risk_level": overall_risk_level,
                "active_bottlenecks_count": len(critical_bottlenecks) + len(high_bottlenecks),
                "critical_bottlenecks_count": len(critical_bottlenecks),
                "spof_suppliers_count": len(spof_suppliers),
                "critical_suppliers_count": len(critical_suppliers),
                "affected_production_lots": lots_impact["summary"]["total_lots"],
                "high_priority_affected_lots": lots_impact["summary"]["high_priority_lots"],
                "average_predicted_delay_hours": lots_impact["summary"]["average_predicted_delay_hours"],
                "active_disruptions_count": len(disruptions)
            },
            "critical_alerts": [
                {
                    "type": "DISRUPTION",
                    "severity": d["severity"],
                    "target_name": d["target_name"],
                    "description": d["description"]
                }
                for d in disruptions
            ] + [
                {
                    "type": "BOTTLENECK",
                    "severity": "CRITICAL",
                    "target_name": b["tool_id"],
                    "description": f"WIP queue at {b['utilization_pct']:.0f}% capacity ({b['current_wip']}/{b['nominal_capacity']} wafers)."
                }
                for b in critical_bottlenecks[:2]
            ] + [
                {
                    "type": "SUPPLIER_SPOF",
                    "severity": "CRITICAL",
                    "target_name": s["name"],
                    "description": f"{s['dependency_pct']}% dependency for {s['material']} with no dual source."
                }
                for s in spof_suppliers[:2]
            ],
            "top_mitigations": [
                {
                    "id": r["id"],
                    "priority": r["priority"],
                    "title": r["title"],
                    "action": r["action"],
                    "reason": r["reason"],
                    "expected_benefit": r["expected_benefit"]
                }
                for r in recs["recommendations"][:4]
            ]
        }
    except Exception as e:
        return {"status": "error", "message": f"Failed to generate executive summary: {str(e)}"}

def run_server():
    """Starts the Nexora MCP Server with standard STDIO transport."""
    print("Starting Nexora MCP Server for IBM Bob over STDIO transport...", file=sys.stderr)
    mcp.run(transport="stdio")

if __name__ == "__main__":
    run_server()
