"""
Nexora — Production Lot Impact & Delivery Prediction Service
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

from datetime import datetime, timedelta
from src.backend.models.database import query_db
from src.backend.ml.predict_delivery import predict_delay_hours

def get_production_lots_impact(filter_priority=None, filter_process=None, filter_tool=None):
    """
    Retrieves active production lots enriched with ML-predicted delivery delays,
    downstream impact, revised completion dates, and urgency ranking.
    """
    query = "SELECT * FROM production_lots WHERE 1=1"
    args = []
    if filter_priority:
        query += " AND priority = ?"
        args.append(filter_priority.upper())
    if filter_process:
        query += " AND current_process_id = ?"
        args.append(filter_process)
    if filter_tool:
        query += " AND assigned_tool_id = ?"
        args.append(filter_tool)
        
    query += " ORDER BY due_date ASC"
    lots = query_db(query, args)
    
    # Pre-fetch tools and routes for fast enrichment
    equipment = {eq["tool_id"]: eq for eq in query_db("SELECT * FROM equipment")}
    routes = {r["process_id"]: r for r in query_db("SELECT * FROM process_routes")}
    
    results = []
    total_wafers = 0
    total_delay_sum = 0
    high_priority_count = 0

    for lot in lots:
        tid = lot["assigned_tool_id"]
        pid = lot["current_process_id"]
        eq = equipment.get(tid, {})
        route = routes.get(pid, {})
        
        cap = eq.get("nominal_capacity", 40)
        wip = eq.get("current_wip", 40)
        util = (wip / cap * 100) if cap > 0 else 100
        stages_remaining = max(1, lot["total_steps"] - lot["steps_completed"])
        
        # Priority mapping
        pri_map = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
        pri_num = pri_map.get(lot["priority"], 2)
        if lot["priority"] in ("HIGH", "CRITICAL"):
            high_priority_count += 1
            
        pred = predict_delay_hours({
            "tool_nominal_capacity": cap,
            "wip_queue_size": wip,
            "tool_utilization_pct": util,
            "downstream_queue_size": stages_remaining * 12,
            "wafer_quantity": lot["wafer_quantity"],
            "lot_priority_num": pri_num,
            "remaining_stages": stages_remaining,
            "nominal_cycle_time_hr": route.get("nominal_cycle_time_hr", 5.0),
            "chamber_health": eq.get("chamber_health", 90),
            "has_active_disruption": 1 if eq.get("status") != "RUNNING" else 0
        })
        
        delay_hrs = pred["predicted_delay_hours"]
        total_delay_sum += delay_hrs
        total_wafers += lot["wafer_quantity"]
        
        # Calculate revised completion
        try:
            due_dt = datetime.strptime(lot["due_date"], "%Y-%m-%d %H:%M:%S")
            revised_dt = due_dt + timedelta(hours=delay_hrs)
            revised_str = revised_dt.strftime("%Y-%m-%d %H:%M:%S")
            hours_until_due = (due_dt - datetime(2026, 9, 15, 8, 0, 0)).total_seconds() / 3600.0
        except Exception:
            revised_str = lot["due_date"]
            hours_until_due = 48.0

        # Urgency scoring (higher = more urgent)
        # Combines priority weight and delay vs due window
        urgency_score = round(pri_num * 25.0 + (delay_hrs / max(1.0, hours_until_due)) * 30.0, 1)

        # Impact level
        if delay_hrs >= 24 or (pri_num >= 3 and delay_hrs >= 12):
            impact_level = "CRITICAL"
        elif delay_hrs >= 12 or pri_num >= 3:
            impact_level = "HIGH"
        elif delay_hrs >= 6:
            impact_level = "MEDIUM"
        else:
            impact_level = "LOW"

        results.append({
            "lot_id": lot["lot_id"],
            "product_family": lot["product_family"],
            "customer_tier": lot["customer_tier"],
            "current_process_id": pid,
            "current_process_name": lot["current_process_name"],
            "next_process_id": lot["next_process_id"],
            "assigned_tool_id": tid,
            "assigned_tool_name": eq.get("name", tid),
            "wafer_quantity": lot["wafer_quantity"],
            "lot_value_usd": lot["lot_value_usd"],
            "priority": lot["priority"],
            "status": lot["status"],
            "entry_time": lot["entry_time"],
            "original_due_date": lot["due_date"],
            "revised_due_date": revised_str,
            "predicted_delay_hours": delay_hrs,
            "impact_level": impact_level,
            "urgency_score": urgency_score,
            "steps_completed": lot["steps_completed"],
            "total_steps": lot["total_steps"],
            "prediction_method": pred["method"],
            "prediction_confidence": pred["confidence_level"],
            "feature_contributions": pred["feature_contributions"]
        })

    # Sort by urgency score descending
    results.sort(key=lambda x: x["urgency_score"], reverse=True)
    
    avg_delay = round(total_delay_sum / max(1, len(results)), 1)
    
    summary = {
        "total_lots": len(results),
        "total_wafers": total_wafers,
        "high_priority_lots": high_priority_count,
        "average_predicted_delay_hours": avg_delay,
        "critical_impact_lots": sum(1 for l in results if l["impact_level"] == "CRITICAL"),
        "high_impact_lots": sum(1 for l in results if l["impact_level"] == "HIGH")
    }

    return {"summary": summary, "lots": results}

def get_lot_by_id(lot_id):
    """
    Retrieves detailed impact profile for a single lot.
    """
    data = get_production_lots_impact()
    return next((l for l in data["lots"] if l["lot_id"] == lot_id), None)
