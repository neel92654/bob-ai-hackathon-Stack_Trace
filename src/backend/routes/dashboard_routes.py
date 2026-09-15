"""
Nexora — Executive Dashboard Summary REST API
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

from flask import Blueprint, jsonify
from src.backend.services.bottleneck_service import get_all_bottlenecks
from src.backend.services.supplier_risk_service import get_all_suppliers_risk, get_geopolitical_summary
from src.backend.services.delivery_prediction_service import get_production_lots_impact
from src.backend.services.recommendation_service import generate_recommendations
from src.backend.models.database import query_db

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/summary", methods=["GET"])
def get_dashboard_summary():
    """
    Returns executive overview metrics:
      - Overall operational risk score & rating
      - Active and critical bottlenecks
      - High-risk & SPoF suppliers
      - Production lot impact & predicted delay
      - Active disruptions & critical alerts
      - Top prioritized recommendations
    """
    bottlenecks = get_all_bottlenecks()
    suppliers = get_all_suppliers_risk()
    lots_impact = get_production_lots_impact()
    recs = generate_recommendations()
    disruptions = query_db("SELECT * FROM disruptions WHERE status = 'ACTIVE'")
    geo_summary = get_geopolitical_summary()

    critical_bottlenecks = [b for b in bottlenecks if b["risk_level"] == "CRITICAL"]
    high_bottlenecks = [b for b in bottlenecks if b["risk_level"] == "HIGH"]
    
    spof_suppliers = [s for s in suppliers if s["is_single_point_of_failure"]]
    critical_suppliers = [s for s in suppliers if s["risk_level"] == "CRITICAL"]
    high_risk_suppliers = [s for s in suppliers if s["risk_level"] in ("CRITICAL", "HIGH")]

    # Overall Operational Risk Score (0-100)
    # 40% Bottleneck pressure + 35% Supply chain SPoF + 25% Disruption exposure
    bottleneck_risk_index = min(100.0, len(critical_bottlenecks) * 35.0 + len(high_bottlenecks) * 15.0)
    supplier_risk_index = min(100.0, len(spof_suppliers) * 25.0 + len(critical_suppliers) * 20.0)
    disruption_risk_index = min(100.0, len(disruptions) * 30.0)
    
    overall_risk_score = round(
        bottleneck_risk_index * 0.40 +
        supplier_risk_index * 0.35 +
        disruption_risk_index * 0.25,
        1
    )
    
    if overall_risk_score >= 75:
        overall_risk_level = "CRITICAL"
    elif overall_risk_score >= 50:
        overall_risk_level = "HIGH"
    elif overall_risk_score >= 25:
        overall_risk_level = "MEDIUM"
    else:
        overall_risk_level = "LOW"

    # Distribution summaries for charts
    bottleneck_distribution = {
        "CRITICAL": len(critical_bottlenecks),
        "HIGH": len(high_bottlenecks),
        "MEDIUM": sum(1 for b in bottlenecks if b["risk_level"] == "MEDIUM"),
        "LOW": sum(1 for b in bottlenecks if b["risk_level"] == "LOW")
    }
    
    supplier_distribution = {
        "CRITICAL": len(critical_suppliers),
        "HIGH": sum(1 for s in suppliers if s["risk_level"] == "HIGH"),
        "MEDIUM": sum(1 for s in suppliers if s["risk_level"] == "MEDIUM"),
        "LOW": sum(1 for s in suppliers if s["risk_level"] == "LOW")
    }

    alerts = []
    for d in disruptions:
        alerts.append({
            "type": "DISRUPTION",
            "severity": d["severity"],
            "title": f"Active Disruption: {d['target_name']}",
            "message": d["description"],
            "time": d["start_time"]
        })
    for b in critical_bottlenecks:
        alerts.append({
            "type": "BOTTLENECK",
            "severity": "CRITICAL",
            "title": f"Critical Tool Queue: {b['tool_id']}",
            "message": f"WIP queue at {b['utilization_pct']:.0f}% capacity ({b['current_wip']}/{b['nominal_capacity']} wafers).",
            "time": "Real-time"
        })
    for s in spof_suppliers:
        alerts.append({
            "type": "SUPPLIER_SPOF",
            "severity": "CRITICAL",
            "title": f"Single Point of Failure: {s['name']}",
            "message": f"{s['dependency_pct']}% dependency for {s['material']} with no dual source.",
            "time": "Real-time"
        })

    return jsonify({
        "status": "success",
        "timestamp": "2026-09-15 08:30:00",
        "kpi_metrics": {
            "overall_operational_risk_score": overall_risk_score,
            "overall_operational_risk_level": overall_risk_level,
            "active_bottlenecks_count": len(critical_bottlenecks) + len(high_bottlenecks),
            "critical_bottlenecks_count": len(critical_bottlenecks),
            "high_risk_suppliers_count": len(high_risk_suppliers),
            "spof_suppliers_count": len(spof_suppliers),
            "affected_production_lots": lots_impact["summary"]["total_lots"],
            "high_priority_affected_lots": lots_impact["summary"]["high_priority_lots"],
            "average_predicted_delay_hours": lots_impact["summary"]["average_predicted_delay_hours"],
            "active_disruptions_count": len(disruptions)
        },
        "distributions": {
            "bottlenecks": bottleneck_distribution,
            "suppliers": supplier_distribution
        },
        "critical_alerts": alerts[:8],
        "top_bottlenecks": bottlenecks[:5],
        "top_suppliers": suppliers[:5],
        "top_recommendations": recs["recommendations"][:5],
        "geopolitical_summary": geo_summary[:4]
    })
