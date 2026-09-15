"""
Nexora — Grounded Operational Decision Assistant Service
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)

Provides grounded, explainable natural-language responses strictly based on current
system data, fab metrics, supplier dependencies, and simulation models.
"""

import re
from src.backend.services.bottleneck_service import get_all_bottlenecks, get_bottleneck_by_id
from src.backend.services.supplier_risk_service import get_all_suppliers_risk, get_supplier_by_id, get_geopolitical_summary
from src.backend.services.delivery_prediction_service import get_production_lots_impact
from src.backend.services.simulation_service import simulate_disruption
from src.backend.models.database import query_db

def process_assistant_query(query_text):
    """
    Parses user query, retrieves real system context, and synthesizes structured operational answers:
      - Direct Answer
      - Supporting Facts
      - Operational Reasoning
      - Recommended Actions
    """
    if not query_text or not isinstance(query_text, str):
        return {
            "query": query_text,
            "direct_answer": "Please provide a valid query regarding fab equipment, suppliers, lots, or simulation scenarios.",
            "supporting_facts": [],
            "reasoning": "No query input was detected.",
            "recommended_action": "Ask about a specific tool (e.g., CVD-03), supplier (e.g., SUP-002), or what-if scenario."
        }

    q = query_text.strip().lower()
    
    # 1. Check for specific Tool Bottleneck query (e.g., "Why is CVD-03 critical?", "Status of LITH-01")
    tool_match = re.search(r'\b(cvd-\d+|lith-\d+|etch-\d+|cmp-\d+|imp-\d+|pvd-\d+|met-\d+|cln-\d+|thm-\d+|pkg-\d+)\b', q)
    if tool_match and ("why" in q or "status" in q or "critical" in q or "bottleneck" in q or "explain" in q or "detail" in q):
        tool_id = tool_match.group(1).upper()
        tool = get_bottleneck_by_id(tool_id)
        if tool:
            return {
                "query": query_text,
                "direct_answer": (
                    f"{tool['tool_id']} ({tool['name']}) is currently classified as {tool['risk_level']} "
                    f"with a queue utilization of {tool['utilization_pct']:.1f}% ({tool['current_wip']} / {tool['nominal_capacity']} nominal capacity)."
                ),
                "supporting_facts": [
                    f"WIP Queue: {tool['current_wip']} wafers (Rated capacity: {tool['nominal_capacity']} wafers).",
                    f"Queue Overload: {tool['queue_pressure']} wafers above rated limit.",
                    f"Affected Production Lots: {tool['affected_lot_count']} lots ({tool['high_priority_lot_count']} high-priority).",
                    f"Downstream Process Stages: {len(tool['downstream_processes'])} stages affected ({', '.join(tool['downstream_processes'][:3])}).",
                    f"ML Predicted Delay: {tool['predicted_delay_hours']} hours."
                ],
                "reasoning": (
                    f"Operating at {tool['utilization_pct']:.0f}% capacity creates back-pressure upstream and starves downstream stages. "
                    f"Chamber health is currently at {tool['chamber_health']}%, with maintenance due in {tool['maintenance_due_hours']} hours."
                ),
                "recommended_action": (
                    f"Prioritize high-value lots and evaluate dynamic capacity reallocation to alternate "
                    f"tools in {tool['process_name']}."
                )
            }

    # 2. Check for Top Bottlenecks query (e.g., "What are the top bottlenecks?", "Where is the bottleneck?")
    if "top" in q and ("bottleneck" in q or "tool" in q or "equipment" in q) or "where is" in q:
        bottlenecks = get_all_bottlenecks()
        top_3 = bottlenecks[:3]
        facts = [
            f"1. {b['tool_id']} ({b['name']}) — {b['risk_level']} ({b['utilization_pct']:.0f}% utilization, {b['affected_lot_count']} lots)"
            for b in top_3
        ]
        return {
            "query": query_text,
            "direct_answer": f"The top {len(top_3)} fab bottlenecks currently are {', '.join([b['tool_id'] for b in top_3])}.",
            "supporting_facts": facts,
            "reasoning": (
                f"{top_3[0]['tool_id']} presents the highest risk due to {top_3[0]['utilization_pct']:.0f}% utilization "
                f"causing a projected {top_3[0]['predicted_delay_hours']}h delay across {top_3[0]['affected_lot_count']} lots."
            ),
            "recommended_action": f"Focus line dispatchers on balancing queue load away from {top_3[0]['tool_id']} immediately."
        }

    # 3. Check for What-If Simulation question (e.g., "What happens if SUP-002 becomes unavailable for 14 days?")
    if ("what happens if" in q or "simulate" in q or "unavailable" in q or "disruption" in q) and "sup-" in q:
        supp_match = re.search(r'\b(sup-\d+)\b', q)
        supplier_id = supp_match.group(1).upper() if supp_match else "SUP-002"
        
        # Extract days if present
        days_match = re.search(r'(\d+)\s*days?', q)
        duration_days = int(days_match.group(1)) if days_match else 14
        
        try:
            sim_res = simulate_disruption("SUPPLIER_DISRUPTION", {
                "supplier_id": supplier_id,
                "duration_days": duration_days
            })
            return {
                "query": query_text,
                "direct_answer": (
                    f"If {sim_res['parameters']['supplier_name']} ({supplier_id}) is disrupted for {duration_days} days, "
                    f"supplier risk surges to CRITICAL (Score: {sim_res['simulated']['supplier_risk_score']}/100), "
                    f"affecting {sim_res['simulated']['affected_lots_count']} production lots with ${sim_res['simulated']['business_exposure_usd']:,.0f} business exposure."
                ),
                "supporting_facts": [
                    f"Material Impacted: {sim_res['parameters']['material']} sourced from {sim_res['parameters']['country']}.",
                    f"Affected Production Lots: {sim_res['simulated']['affected_lots_count']} lots ({sim_res['simulated']['wafers_at_risk']} wafers at risk).",
                    f"Delivery Delay: Projected average delay increases from {sim_res['baseline']['predicted_delay_hours']}h to {sim_res['simulated']['predicted_delay_hours']}h (+{sim_res['delta']['delay_increase_hours']}h).",
                    f"Estimated Financial Exposure: ${sim_res['simulated']['business_exposure_usd']:,.0f}."
                ],
                "reasoning": (
                    f"{supplier_id} supplies critical material with high dependency and no instant dual-source backup. "
                    f"A {duration_days}-day outage exhausts existing safety stock buffers and directly throttles downstream stages."
                ),
                "recommended_action": (
                    f"Activate emergency safety stock protocol and initiate fast-track qualification for backup sources."
                )
            }
        except Exception as e:
            pass

    # 4. Check for Specific Supplier query (e.g., "Why is supplier SUP-002 critical?", "Which supplier is the biggest risk?")
    supp_match = re.search(r'\b(sup-\d+)\b', q)
    if supp_match or ("supplier" in q and ("biggest" in q or "risk" in q or "critical" in q or "spof" in q or "single point" in q)):
        if supp_match:
            supplier_id = supp_match.group(1).upper()
            supplier = get_supplier_by_id(supplier_id)
        else:
            all_s = get_all_suppliers_risk()
            supplier = all_s[0] if all_s else None

        if supplier:
            return {
                "query": query_text,
                "direct_answer": (
                    f"{supplier['supplier_id']} ({supplier['name']}) is rated {supplier['risk_level']} "
                    f"with an explainable risk score of {supplier['supplier_risk_score']}/100."
                ),
                "supporting_facts": [
                    f"Material: {supplier['material']} ({supplier['criticality']} criticality).",
                    f"Dependency Share: {supplier['dependency_pct']}% of total fab requirement.",
                    f"Procurement Lead Time: {supplier['lead_time_days']} days from {supplier['country']}.",
                    f"Alternate Supplier: {supplier['alternate_supplier']} ({supplier['alternate_capacity_pct']}% available capacity).",
                    f"Single Point of Failure (SPoF): {'YES' if supplier['is_single_point_of_failure'] else 'NO'}."
                ],
                "reasoning": (
                    f"Risk score is driven by: " + "; ".join(supplier["risk_reasons"]) + "."
                ),
                "recommended_action": (
                    f"Qualify secondary supplier ({supplier['alternate_supplier']}) and increase safety stock buffer."
                )
            }

    # 5. Check for Production Lot Prioritization (e.g., "Which lots should we prioritize?", "Delivery impact")
    if "prioritize" in q or "lots" in q or "delivery" in q or "impact" in q:
        lots_data = get_production_lots_impact()
        top_lots = lots_data["lots"][:3]
        facts = [
            f"• {l['lot_id']} ({l['product_family']}) — Priority: {l['priority']}, Due: {l['original_due_date'][:10]}, Predicted Delay: +{l['predicted_delay_hours']}h (Urgency Score: {l['urgency_score']})"
            for l in top_lots
        ]
        return {
            "query": query_text,
            "direct_answer": (
                f"We recommend prioritizing high-urgency lots: {', '.join([l['lot_id'] for l in top_lots])}. "
                f"Average predicted delay across active fab lots is {lots_data['summary']['average_predicted_delay_hours']} hours."
            ),
            "supporting_facts": facts,
            "reasoning": (
                f"These lots have high value commitments (${sum(l['lot_value_usd'] for l in top_lots):,.0f} combined) "
                f"and are currently queued in high-utilization bottleneck stages."
            ),
            "recommended_action": "Apply expedited dispatch tags to top-urgency lots and re-route around bottlenecked tools."
        }

    # 6. Check for Geopolitical questions
    if "geopolitical" in q or "country" in q or "concentration" in q:
        geo = get_geopolitical_summary()
        top_geo = geo[:2]
        facts = [
            f"• {g['country']}: {g['supplier_count']} suppliers, {g['average_dependency_pct']}% avg dependency, Critical materials: {', '.join(g['critical_materials']) or 'None'}"
            for g in top_geo
        ]
        return {
            "query": query_text,
            "direct_answer": (
                f"The highest geopolitical concentration risk resides in {top_geo[0]['country']} "
                f"({top_geo[0]['concentration_level']} concentration, {top_geo[0]['average_dependency_pct']}% avg dependency)."
            ),
            "supporting_facts": facts,
            "reasoning": (
                f"{top_geo[0]['country']} supplies critical items like {', '.join(top_geo[0]['critical_materials']) or 'key chemicals'} "
                f"with limited regional diversification."
            ),
            "recommended_action": "Diversify procurement channels to geographically distinct suppliers in North America and Europe."
        }

    # Default fallback for questions outside the data boundary
    return {
        "query": query_text,
        "direct_answer": "That information is not available in the current Nexora data.",
        "supporting_facts": [
            "Nexora provides grounded intelligence on fab bottlenecks (tools), suppliers, production lots, disruptions, and what-if simulations."
        ],
        "reasoning": "The query does not match any tracked fab equipment, supplier record, lot ID, or simulation parameters.",
        "recommended_action": "Try asking: 'Why is CVD-03 critical?', 'Which supplier is the biggest risk?', or 'What happens if SUP-002 becomes unavailable for 14 days?'"
    }
