"""
Nexora — Prioritized Operational Recommendation Engine
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)

Synthesizes actionable, explainable operational recommendations grounded strictly
in current fab bottleneck conditions, SPoF supplier exposures, and active disruptions.
"""

from src.backend.services.bottleneck_service import get_all_bottlenecks
from src.backend.services.supplier_risk_service import get_all_suppliers_risk
from src.backend.models.database import query_db

def generate_recommendations(category_filter=None, priority_filter=None):
    """
    Generates rule-based, condition-driven recommendations with operational justification.
    """
    bottlenecks = get_all_bottlenecks()
    suppliers = get_all_suppliers_risk()
    disruptions = query_db("SELECT * FROM disruptions WHERE status = 'ACTIVE'")

    recommendations = []
    rec_id = 1

    # 1. Evaluate Active Disruptions
    for d in disruptions:
        recommendations.append({
            "id": f"REC-{rec_id:03d}",
            "category": "DISRUPTION_MITIGATION",
            "priority": "CRITICAL" if d["severity"] == "CRITICAL" else "HIGH",
            "target_type": d["target_type"],
            "target_id": d["target_id"],
            "target_name": d["target_name"],
            "title": f"Mitigate Active Event: {d['disruption_id']}",
            "action": d["recommended_mitigation"],
            "reason": d["impact_summary"],
            "expected_benefit": "Restores operational stability and contains schedule slippage.",
            "urgency_badge": "IMMEDIATE ACTION REQUIRED"
        })
        rec_id += 1

    # 2. Evaluate Critical & High Bottlenecks
    critical_tools = [b for b in bottlenecks if b["risk_level"] in ("CRITICAL", "HIGH")]
    for tool in critical_tools:
        tid = tool["tool_id"]
        util = tool["utilization_pct"]
        lots_count = tool["affected_lot_count"]
        high_pri_lots = tool["high_priority_lot_count"]
        
        # Check alternate tools in same process
        alt_tools = [b["tool_id"] for b in bottlenecks if b["process_id"] == tool["process_id"] and b["tool_id"] != tid and b["risk_level"] in ("LOW", "MEDIUM")]
        
        if tool["risk_level"] == "CRITICAL":
            action_text = (
                f"Reallocate 35% lot volume to {', '.join(alt_tools)}" if alt_tools 
                else f"Trigger emergency capacity overtime and expedite lot processing on {tid}"
            )
            recommendations.append({
                "id": f"REC-{rec_id:03d}",
                "category": "FAB_BOTTLENECK",
                "priority": "CRITICAL",
                "target_type": "EQUIPMENT",
                "target_id": tid,
                "target_name": tool["name"],
                "title": f"Clear Critical Queue Pressure on {tid}",
                "action": action_text,
                "reason": f"WIP queue is at {util:.0f}% capacity ({lots_count} lots affected, {high_pri_lots} high-priority). Downstream processes face starvation.",
                "expected_benefit": f"Reduces projected delivery delay by up to {tool['predicted_delay_hours'] * 0.45:.1f} hours.",
                "urgency_badge": "LINE STABILITY RISK"
            })
            rec_id += 1
            
            # Chamber health maintenance check
            if tool["chamber_health"] < 80 or tool["maintenance_due_hours"] < 48:
                recommendations.append({
                    "id": f"REC-{rec_id:03d}",
                    "category": "PREVENTIVE_MAINTENANCE",
                    "priority": "HIGH",
                    "target_type": "EQUIPMENT",
                    "target_id": tid,
                    "target_name": tool["name"],
                    "title": f"Schedule Immediate Preventive Chamber Service on {tid}",
                    "action": f"Execute scheduled maintenance cycle within next {tool['maintenance_due_hours']} hours.",
                    "reason": f"Chamber health is at {tool['chamber_health']}%, risking unplanned tool breakdown under heavy WIP.",
                    "expected_benefit": "Prevents catastrophic line outage and preserves wafer yield.",
                    "urgency_badge": "RELIABILITY GUARD"
                })
                rec_id += 1
        elif tool["risk_level"] == "HIGH":
            recommendations.append({
                "id": f"REC-{rec_id:03d}",
                "category": "FAB_BOTTLENECK",
                "priority": "HIGH",
                "target_type": "EQUIPMENT",
                "target_id": tid,
                "target_name": tool["name"],
                "title": f"Balance Tool Load on {tid}",
                "action": f"Prioritize dispatching high-margin lots while queue utilization stands at {util:.0f}%.",
                "reason": f"Tool operates {tool['queue_pressure']} units above nominal rating.",
                "expected_benefit": "Averts escalation into critical bottleneck status.",
                "urgency_badge": "LOAD BALANCING"
            })
            rec_id += 1

    # 3. Evaluate Single Point of Failure (SPoF) & Critical Suppliers
    spof_suppliers = [s for s in suppliers if s["is_single_point_of_failure"] or s["risk_level"] == "CRITICAL"]
    for supp in spof_suppliers:
        sid = supp["supplier_id"]
        dep = supp["dependency_pct"]
        mat = supp["material"]
        alt = supp["alternate_supplier"]
        
        if supp["is_single_point_of_failure"]:
            recommendations.append({
                "id": f"REC-{rec_id:03d}",
                "category": "SUPPLY_CHAIN_SPOF",
                "priority": "CRITICAL",
                "target_type": "SUPPLIER",
                "target_id": sid,
                "target_name": supp["name"],
                "title": f"Qualify Dual-Source Alternative for {mat}",
                "action": f"Initiate procurement qualification of backup vendor (Current: {alt}) and increase safety stock to 45 days.",
                "reason": f"Single Point of Failure identified with {dep}% reliance on {supp['name']} ({supp['country']}) for {mat}.",
                "expected_benefit": "Eliminates single-point supply vulnerability and insulates fab against geopolitical export shifts.",
                "urgency_badge": "CRITICAL SPoF"
            })
            rec_id += 1
        elif supp["risk_level"] == "HIGH":
            recommendations.append({
                "id": f"REC-{rec_id:03d}",
                "category": "SUPPLY_CHAIN_RISK",
                "priority": "HIGH",
                "target_type": "SUPPLIER",
                "target_id": sid,
                "target_name": supp["name"],
                "title": f"Buffer Lead Time & Review Terms for {supp['name']}",
                "action": f"Extend order lead time horizon to {supp['lead_time_days'] + 10} days and negotiate reservation capacity.",
                "reason": f"Explainable risk score is {supp['supplier_risk_score']}/100 with {dep}% dependency in {supp['country']}.",
                "expected_benefit": "Maintains raw material availability margin.",
                "urgency_badge": "SUPPLY BUFFER"
            })
            rec_id += 1

    # Filtering
    if category_filter:
        recommendations = [r for r in recommendations if r["category"].upper() == category_filter.upper()]
    if priority_filter:
        recommendations = [r for r in recommendations if r["priority"].upper() == priority_filter.upper()]

    # Sort priority order
    priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    recommendations.sort(key=lambda x: priority_order.get(x["priority"], 4))

    return {
        "total_recommendations": len(recommendations),
        "critical_count": sum(1 for r in recommendations if r["priority"] == "CRITICAL"),
        "high_count": sum(1 for r in recommendations if r["priority"] == "HIGH"),
        "recommendations": recommendations
    }
