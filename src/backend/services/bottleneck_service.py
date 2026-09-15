"""
Nexora — Fab Bottleneck Intelligence Service
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

from src.backend.models.database import query_db
from src.backend.utils.calculations import calculate_bottleneck_metrics
from src.backend.ml.predict_delivery import predict_delay_hours

def get_all_bottlenecks():
    """
    Retrieves all equipment with dynamic bottleneck metrics, queue pressure,
    affected lot counts, downstream process impact, and explainability text.
    """
    equipment_list = query_db("SELECT * FROM equipment ORDER BY tool_id")
    routes = query_db("SELECT * FROM process_routes ORDER BY step_seq")
    route_map = {r["process_id"]: r for r in routes}
    
    # Pre-aggregate lots by assigned tool
    lots = query_db("SELECT * FROM production_lots")
    tool_lots_map = {}
    for lot in lots:
        tid = lot["assigned_tool_id"]
        if tid not in tool_lots_map:
            tool_lots_map[tid] = []
        tool_lots_map[tid].append(lot)

    results = []
    for eq in equipment_list:
        tid = eq["tool_id"]
        pid = eq["process_id"]
        curr_route = route_map.get(pid, {})
        curr_seq = curr_route.get("step_seq", 1)
        
        assigned_lots = tool_lots_map.get(tid, [])
        affected_count = len(assigned_lots)
        affected_wafers = sum(l["wafer_quantity"] for l in assigned_lots)
        high_priority_count = sum(1 for l in assigned_lots if l["priority"] in ("HIGH", "CRITICAL"))
        
        metrics = calculate_bottleneck_metrics(
            nominal_capacity=eq["nominal_capacity"],
            current_wip=eq["current_wip"],
            tool_id=tid,
            affected_lot_count=affected_count
        )
        
        # Determine downstream processes
        downstream_processes = [
            r["name"] for r in routes if r["step_seq"] > curr_seq
        ]
        
        # Calculate delivery prediction for this tool's average lot
        pred = predict_delay_hours({
            "tool_nominal_capacity": eq["nominal_capacity"],
            "wip_queue_size": eq["current_wip"],
            "tool_utilization_pct": metrics["utilization_pct"],
            "downstream_queue_size": len(downstream_processes) * 15,
            "wafer_quantity": 50,
            "lot_priority_num": 3 if high_priority_count > 0 else 2,
            "remaining_stages": len(downstream_processes),
            "nominal_cycle_time_hr": curr_route.get("nominal_cycle_time_hr", 5.0),
            "chamber_health": eq["chamber_health"],
            "has_active_disruption": 1 if eq["status"] != "RUNNING" else 0
        })

        results.append({
            "tool_id": tid,
            "name": eq["name"],
            "process_id": pid,
            "process_name": curr_route.get("name", pid),
            "step_seq": curr_seq,
            "nominal_capacity": eq["nominal_capacity"],
            "current_wip": eq["current_wip"],
            "utilization_pct": metrics["utilization_pct"],
            "queue_pressure": metrics["queue_pressure"],
            "risk_level": metrics["risk_level"],
            "risk_score": metrics["risk_score"],
            "explanation": metrics["explanation"],
            "status": eq["status"],
            "chamber_health": eq["chamber_health"],
            "maintenance_due_hours": eq["maintenance_due_hours"],
            "mtbf_hours": eq["mtbf_hours"],
            "affected_lot_count": affected_count,
            "affected_wafer_count": affected_wafers,
            "high_priority_lot_count": high_priority_count,
            "downstream_processes": downstream_processes,
            "predicted_delay_hours": pred["predicted_delay_hours"],
            "prediction_method": pred["method"],
            "prediction_confidence": pred["confidence_level"]
        })

    # Sort so CRITICAL and HIGH bottlenecks appear first, then highest utilization
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    results.sort(key=lambda x: (severity_order.get(x["risk_level"], 4), -x["utilization_pct"]))
    return results

def get_bottleneck_by_id(tool_id):
    """
    Retrieves detailed bottleneck analytics for a specific tool ID, including full process path and assigned lots.
    """
    all_bottlenecks = get_all_bottlenecks()
    target = next((b for b in all_bottlenecks if b["tool_id"] == tool_id), None)
    if not target:
        return None
    
    # Fetch all assigned production lots
    assigned_lots = query_db("SELECT * FROM production_lots WHERE assigned_tool_id = ? ORDER BY due_date ASC", (tool_id,))
    target["assigned_lots"] = assigned_lots
    
    # Process route roadmap for visual timeline
    routes = query_db("SELECT * FROM process_routes ORDER BY step_seq")
    target["process_roadmap"] = [
        {
            "step_seq": r["step_seq"],
            "process_id": r["process_id"],
            "name": r["name"],
            "is_current": r["process_id"] == target["process_id"],
            "is_downstream": r["step_seq"] > target["step_seq"]
        }
        for r in routes
    ]
    return target
