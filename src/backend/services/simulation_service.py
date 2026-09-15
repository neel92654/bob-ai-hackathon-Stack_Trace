"""
Nexora — What-If Disruption Simulation Engine
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)

Simulates 4 core operational disruption scenarios:
  1. Supplier Disruption (geopolitical export embargo, logistic shutdown)
  2. Equipment Failure (unscheduled breakdown, chamber maintenance)
  3. Capacity Reduction (maintenance derating, yield degradation)
  4. Demand Surge (sudden wafer volume influx)

Produces structured Before vs. After metrics diffs and prioritized response protocols.
"""

from src.backend.models.database import query_db
from src.backend.utils.calculations import (
    calculate_bottleneck_metrics,
    calculate_supplier_risk_score
)
from src.backend.ml.predict_delivery import predict_delay_hours

def simulate_disruption(scenario_type, params):
    """
    Dispatcher for the 4 What-If simulation scenarios.
    """
    scenario_type = scenario_type.upper()
    if scenario_type == "SUPPLIER_DISRUPTION":
        return _simulate_supplier_disruption(params)
    elif scenario_type == "EQUIPMENT_FAILURE":
        return _simulate_equipment_failure(params)
    elif scenario_type == "CAPACITY_REDUCTION":
        return _simulate_capacity_reduction(params)
    elif scenario_type == "DEMAND_INCREASE":
        return _simulate_demand_increase(params)
    else:
        raise ValueError(f"Unknown scenario type: {scenario_type}. Must be SUPPLIER_DISRUPTION, EQUIPMENT_FAILURE, CAPACITY_REDUCTION, or DEMAND_INCREASE.")

def _simulate_supplier_disruption(params):
    supplier_id = params.get("supplier_id", "SUP-002")
    duration_days = int(params.get("duration_days", 14))
    
    supplier = query_db("SELECT * FROM suppliers WHERE supplier_id = ?", (supplier_id,), one=True)
    if not supplier:
        raise ValueError(f"Supplier ID '{supplier_id}' not found.")
        
    pids = [p.strip() for p in supplier["affected_process_ids"].split(",") if p.strip()]
    placeholders = ", ".join(["?"] * len(pids)) if pids else "''"
    affected_lots = query_db(f"SELECT * FROM production_lots WHERE current_process_id IN ({placeholders})", pids)
    
    total_wafers = sum(l["wafer_quantity"] for l in affected_lots)
    total_lot_value = sum(l["lot_value_usd"] for l in affected_lots)
    high_priority_lots = sum(1 for l in affected_lots if l["priority"] in ("HIGH", "CRITICAL"))
    
    # Baseline supplier risk
    base_risk = calculate_supplier_risk_score(supplier)
    
    # Simulated supplier risk under active shutdown
    sim_supplier = dict(supplier)
    sim_supplier["dependency_pct"] = min(100, sim_supplier["dependency_pct"] + 15)
    sim_supplier["lead_time_days"] = sim_supplier["lead_time_days"] + duration_days
    sim_supplier["geo_risk_factor"] = min(2.0, sim_supplier["geo_risk_factor"] + 0.3)
    sim_risk = calculate_supplier_risk_score(sim_supplier)
    
    # Delay impacts
    baseline_avg_delay = 4.2
    simulated_additional_delay_hr = round(duration_days * 18.5 * (sim_supplier["dependency_pct"] / 100.0), 1)
    simulated_total_delay_hr = baseline_avg_delay + simulated_additional_delay_hr
    
    # Exposure in USD
    business_exposure_usd = round(total_lot_value * min(1.0, (duration_days / 30.0) * 0.45), 2)

    recommendations = [
        {
            "priority": "CRITICAL",
            "action": f"Activate contingency buffer for {supplier['material']}",
            "reason": f"Primary supplier {supplier['name']} unavailable for {duration_days} days affecting {len(affected_lots)} active production lots.",
            "expected_benefit": "Maintains fab continuity for approximately 10 days of existing safety stock."
        },
        {
            "priority": "HIGH",
            "action": f"Fast-track secondary supplier qualification: {supplier['alternate_supplier']}",
            "reason": f"Alternate supplier has {supplier['alternate_capacity_pct']}% capacity with {supplier['alternate_lead_time_days']} days lead time.",
            "expected_benefit": "Secures secondary line capacity and mitigates single-source dependency."
        },
        {
            "priority": "HIGH",
            "action": "Prioritize Tier-1 Automotive and Hyperscale AI wafer lots",
            "reason": f"{high_priority_lots} high-value lots represent ${business_exposure_usd:,.0f} delivery commitment exposure.",
            "expected_benefit": "Protects SLA-bound enterprise customer contracts."
        }
    ]

    return {
        "scenario": "Supplier Disruption",
        "scenario_type": "SUPPLIER_DISRUPTION",
        "parameters": {
            "supplier_id": supplier_id,
            "supplier_name": supplier["name"],
            "material": supplier["material"],
            "country": supplier["country"],
            "duration_days": duration_days
        },
        "baseline": {
            "supplier_risk_score": base_risk["supplier_risk_score"],
            "risk_level": base_risk["risk_level"],
            "predicted_delay_hours": baseline_avg_delay,
            "affected_lots_count": 0,
            "wafers_at_risk": 0,
            "business_exposure_usd": 0.0
        },
        "simulated": {
            "supplier_risk_score": sim_risk["supplier_risk_score"],
            "risk_level": "CRITICAL",
            "predicted_delay_hours": simulated_total_delay_hr,
            "affected_lots_count": len(affected_lots),
            "wafers_at_risk": total_wafers,
            "business_exposure_usd": business_exposure_usd
        },
        "delta": {
            "risk_score_diff": round(sim_risk["supplier_risk_score"] - base_risk["supplier_risk_score"], 1),
            "delay_increase_hours": simulated_additional_delay_hr,
            "lots_affected_diff": len(affected_lots),
            "exposure_increase_usd": business_exposure_usd
        },
        "affected_processes": pids,
        "recommended_actions": recommendations
    }

def _simulate_equipment_failure(params):
    tool_id = params.get("tool_id", "CVD-03")
    failure_duration_hours = int(params.get("failure_duration_hours", 24))
    
    tool = query_db("SELECT * FROM equipment WHERE tool_id = ?", (tool_id,), one=True)
    if not tool:
        raise ValueError(f"Equipment ID '{tool_id}' not found.")
        
    lots = query_db("SELECT * FROM production_lots WHERE assigned_tool_id = ?", (tool_id,))
    total_wafers = sum(l["wafer_quantity"] for l in lots)
    high_priority_count = sum(1 for l in lots if l["priority"] in ("HIGH", "CRITICAL"))
    
    # Baseline
    base_metrics = calculate_bottleneck_metrics(tool["nominal_capacity"], tool["current_wip"], tool_id, len(lots))
    
    # Alternate tools in the same process
    alt_tools = query_db("SELECT * FROM equipment WHERE process_id = ? AND tool_id != ?", (tool["process_id"], tool_id))
    alt_tool_names = [t["tool_id"] for t in alt_tools]
    
    # Simulated metrics (Tool down, WIP piles up, downstream stalls)
    simulated_wip = tool["current_wip"] + int((failure_duration_hours / 24.0) * 12)
    sim_metrics = calculate_bottleneck_metrics(max(1, int(tool["nominal_capacity"] * 0.1)), simulated_wip, tool_id, len(lots))
    
    # Delay prediction under outage
    pred = predict_delay_hours({
        "tool_nominal_capacity": tool["nominal_capacity"],
        "wip_queue_size": simulated_wip,
        "tool_utilization_pct": 220.0,
        "downstream_queue_size": 45,
        "wafer_quantity": 50,
        "lot_priority_num": 3,
        "remaining_stages": 4,
        "nominal_cycle_time_hr": 7.0,
        "chamber_health": 20,
        "has_active_disruption": 1
    })
    
    simulated_delay = pred["predicted_delay_hours"] + (failure_duration_hours * 0.85)
    simulated_delay = round(simulated_delay, 1)
    
    recommendations = [
        {
            "priority": "CRITICAL",
            "action": f"Reallocate incoming lots to alternate tools: {', '.join(alt_tool_names) if alt_tool_names else 'No alternate tool available'}",
            "reason": f"{tool_id} outage of {failure_duration_hours}h stops processing of {len(lots)} queued lots.",
            "expected_benefit": "Avoids wafer lot queue stagnation and reduces cumulative delay by ~60%."
        },
        {
            "priority": "HIGH",
            "action": f"Dispatch urgent field service on {tool_id}",
            "reason": f"Tool failure halts stage {tool['process_id']} with {total_wafers} wafers in buffer.",
            "expected_benefit": "Restores nominal throughput and prevents downstream process line starvation."
        },
        {
            "priority": "MEDIUM",
            "action": "Hold upstream dispatch from previous process stage",
            "reason": "Prevents catastrophic queue explosion in front of broken tool.",
            "expected_benefit": "Stabilizes line balance."
        }
    ]

    return {
        "scenario": "Equipment Failure",
        "scenario_type": "EQUIPMENT_FAILURE",
        "parameters": {
            "tool_id": tool_id,
            "tool_name": tool["name"],
            "process_id": tool["process_id"],
            "failure_duration_hours": failure_duration_hours
        },
        "baseline": {
            "utilization_pct": base_metrics["utilization_pct"],
            "risk_level": base_metrics["risk_level"],
            "risk_score": base_metrics["risk_score"],
            "current_wip": tool["current_wip"],
            "predicted_delay_hours": 6.5,
            "affected_lots_count": len(lots)
        },
        "simulated": {
            "utilization_pct": 250.0,
            "risk_level": "CRITICAL",
            "risk_score": 98.5,
            "current_wip": simulated_wip,
            "predicted_delay_hours": simulated_delay,
            "affected_lots_count": len(lots) + 6
        },
        "delta": {
            "delay_increase_hours": round(simulated_delay - 6.5, 1),
            "wip_increase": simulated_wip - tool["current_wip"],
            "lots_affected_diff": 6
        },
        "alternate_tools": alt_tool_names,
        "recommended_actions": recommendations
    }

def _simulate_capacity_reduction(params):
    tool_id = params.get("tool_id", "LITH-01")
    reduction_pct = float(params.get("capacity_reduction_pct", 30.0))
    duration_days = int(params.get("duration_days", 7))
    
    tool = query_db("SELECT * FROM equipment WHERE tool_id = ?", (tool_id,), one=True)
    if not tool:
        raise ValueError(f"Equipment ID '{tool_id}' not found.")
        
    lots = query_db("SELECT * FROM production_lots WHERE assigned_tool_id = ?", (tool_id,))
    base_metrics = calculate_bottleneck_metrics(tool["nominal_capacity"], tool["current_wip"], tool_id, len(lots))
    
    # Reduced capacity
    derated_capacity = max(1, int(tool["nominal_capacity"] * (1.0 - reduction_pct / 100.0)))
    sim_metrics = calculate_bottleneck_metrics(derated_capacity, tool["current_wip"], tool_id, len(lots))
    
    pred = predict_delay_hours({
        "tool_nominal_capacity": derated_capacity,
        "wip_queue_size": tool["current_wip"],
        "tool_utilization_pct": sim_metrics["utilization_pct"],
        "downstream_queue_size": 30,
        "wafer_quantity": 50,
        "lot_priority_num": 2,
        "remaining_stages": 6,
        "nominal_cycle_time_hr": 8.0,
        "chamber_health": 75,
        "has_active_disruption": 0
    })

    return {
        "scenario": "Capacity Reduction",
        "scenario_type": "CAPACITY_REDUCTION",
        "parameters": {
            "tool_id": tool_id,
            "tool_name": tool["name"],
            "capacity_reduction_pct": reduction_pct,
            "duration_days": duration_days
        },
        "baseline": {
            "nominal_capacity": tool["nominal_capacity"],
            "utilization_pct": base_metrics["utilization_pct"],
            "risk_level": base_metrics["risk_level"],
            "risk_score": base_metrics["risk_score"],
            "predicted_delay_hours": 3.8
        },
        "simulated": {
            "nominal_capacity": derated_capacity,
            "utilization_pct": sim_metrics["utilization_pct"],
            "risk_level": sim_metrics["risk_level"],
            "risk_score": sim_metrics["risk_score"],
            "predicted_delay_hours": pred["predicted_delay_hours"]
        },
        "delta": {
            "capacity_loss": tool["nominal_capacity"] - derated_capacity,
            "utilization_increase_pct": round(sim_metrics["utilization_pct"] - base_metrics["utilization_pct"], 1),
            "delay_increase_hours": round(pred["predicted_delay_hours"] - 3.8, 1)
        },
        "recommended_actions": [
            {
                "priority": "HIGH" if sim_metrics["risk_level"] in ("CRITICAL", "HIGH") else "MEDIUM",
                "action": f"Shift batch schedules on {tool_id} to off-peak shifts",
                "reason": f"Capacity derated by {reduction_pct}%, pushing utilization to {sim_metrics['utilization_pct']:.0f}%.",
                "expected_benefit": "Absorbs queue accumulation and levels fab load."
            }
        ]
    }

def _simulate_demand_increase(params):
    demand_increase_pct = float(params.get("demand_increase_pct", 25.0))
    duration_weeks = int(params.get("duration_weeks", 4))
    
    all_tools = query_db("SELECT * FROM equipment")
    
    baseline_critical_count = 0
    simulated_critical_count = 0
    base_delays = []
    sim_delays = []
    
    for tool in all_tools:
        base_m = calculate_bottleneck_metrics(tool["nominal_capacity"], tool["current_wip"], tool["tool_id"])
        if base_m["risk_level"] in ("CRITICAL", "HIGH"):
            baseline_critical_count += 1
            
        sim_wip = int(tool["current_wip"] * (1.0 + demand_increase_pct / 100.0))
        sim_m = calculate_bottleneck_metrics(tool["nominal_capacity"], sim_wip, tool["tool_id"])
        if sim_m["risk_level"] in ("CRITICAL", "HIGH"):
            simulated_critical_count += 1
            
        base_pred = predict_delay_hours({
            "tool_nominal_capacity": tool["nominal_capacity"],
            "wip_queue_size": tool["current_wip"],
            "tool_utilization_pct": base_m["utilization_pct"],
            "downstream_queue_size": 25,
            "wafer_quantity": 50,
            "lot_priority_num": 2,
            "remaining_stages": 5,
            "nominal_cycle_time_hr": 5.0,
            "chamber_health": tool["chamber_health"],
            "has_active_disruption": 0
        })
        sim_pred = predict_delay_hours({
            "tool_nominal_capacity": tool["nominal_capacity"],
            "wip_queue_size": sim_wip,
            "tool_utilization_pct": sim_m["utilization_pct"],
            "downstream_queue_size": int(25 * (1.0 + demand_increase_pct / 100.0)),
            "wafer_quantity": 50,
            "lot_priority_num": 2,
            "remaining_stages": 5,
            "nominal_cycle_time_hr": 5.0,
            "chamber_health": tool["chamber_health"],
            "has_active_disruption": 0
        })
        base_delays.append(base_pred["predicted_delay_hours"])
        sim_delays.append(sim_pred["predicted_delay_hours"])

    avg_base_delay = round(sum(base_delays) / max(1, len(base_delays)), 1)
    avg_sim_delay = round(sum(sim_delays) / max(1, len(sim_delays)), 1)

    return {
        "scenario": "Demand Surge",
        "scenario_type": "DEMAND_INCREASE",
        "parameters": {
            "demand_increase_pct": demand_increase_pct,
            "duration_weeks": duration_weeks
        },
        "baseline": {
            "critical_bottlenecks_count": baseline_critical_count,
            "average_predicted_delay_hours": avg_base_delay,
            "fab_capacity_status": "MANAGEABLE"
        },
        "simulated": {
            "critical_bottlenecks_count": simulated_critical_count,
            "average_predicted_delay_hours": avg_sim_delay,
            "fab_capacity_status": "OVERBURDENED" if simulated_critical_count > baseline_critical_count + 3 else "ELEVATED"
        },
        "delta": {
            "additional_bottleneck_tools": simulated_critical_count - baseline_critical_count,
            "delay_increase_hours": round(avg_sim_delay - avg_base_delay, 1)
        },
        "recommended_actions": [
            {
                "priority": "HIGH",
                "action": "Activate auxiliary fab outsourcing & overtime dispatch",
                "reason": f"A {demand_increase_pct}% surge adds {simulated_critical_count - baseline_critical_count} critical tool bottlenecks across the line.",
                "expected_benefit": "Maintains SLA delivery targets without sacrificing wafer yield."
            },
            {
                "priority": "MEDIUM",
                "action": "Increase raw material supplier order forecasts",
                "reason": "Consumables like photoresist and CMP slurry burn rates accelerate under higher WIP load.",
                "expected_benefit": "Prevents stockouts during elevated run rate."
            }
        ]
    }
