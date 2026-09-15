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
    simulated_total_delay_hr = round(baseline_avg_delay + simulated_additional_delay_hr, 1)
    
    # Financial SLA Exposure in USD
    business_exposure_usd = round(total_lot_value * min(1.0, (duration_days / 30.0) * 0.45), 2)
    financial_impact_millions = round(max(0.4, business_exposure_usd / 1_000_000.0), 2)

    has_spof = bool(base_risk.get("is_single_point_of_failure") or supplier.get("single_point_of_failure") == 1)
    has_alt = bool(supplier.get("alternate_supplier") and supplier.get("alternate_supplier") != "None")
    alt_name = supplier["alternate_supplier"] if has_alt else "Secondary Source"
    alt_cap = supplier["alternate_capacity_pct"] if has_alt else 0
    alt_lead = supplier["alternate_lead_time_days"] if has_alt else 90

    # Intelligent Scenario-Specific Primary Mitigation
    if has_spof or alt_cap < 30:
        primary_action = f"Activate strategic inventory rationing & qualify emergency source for {supplier['material']} ({supplier_id})"
    elif has_alt:
        primary_action = f"Reroute {min(100, 100 - alt_cap)}% {supplier['material']} procurement volume to {alt_name}"
    else:
        primary_action = f"Enforce buffer conservation protocol for {supplier['material']} from {supplier['name']}"

    primary_detail = (
        f"A {duration_days}-day outage of {supplier['name']} ({supplier['country']}) impacts {len(affected_lots)} active lots "
        f"({total_wafers:,} wafers) across {len(pids)} fab stages, risking ${financial_impact_millions}M SLA exposure "
        f"with +{simulated_additional_delay_hr:.1f}h projected delay drift."
    )

    operational_impact_summary = (
        f"Disrupting {supplier['name']} ({supplier_id}, {supplier['country']}) for {duration_days} days halts critical supply of "
        f"{supplier['material']} (dependency: {supplier['dependency_pct']}%, base lead time: {supplier['lead_time_days']}d). "
        f"Fab buffer stock will deplete within approx {max(2, int(duration_days * 0.4))} days, causing +{simulated_additional_delay_hr:.1f}h "
        f"downstream delay drift across {', '.join(pids[:3])}{'...' if len(pids) > 3 else ''}."
    )

    # Prioritized Supporting Actions
    recommendations = [
        {
            "priority": "CRITICAL",
            "action": f"Ration on-hand {supplier['material']} buffer for {high_priority_lots} Tier-1 lots",
            "reason": f"Primary supplier {supplier['name']} unavailable for {duration_days} days affecting {len(affected_lots)} active production lots.",
            "expected_benefit": f"Maintains line continuity for high-value orders across ${business_exposure_usd:,.0f} delivery commitments."
        },
        {
            "priority": "HIGH",
            "action": f"Fast-track secondary supplier engagement: {alt_name}",
            "reason": f"Alternate source provides {alt_cap}% volume coverage with {alt_lead} days lead time." if has_alt else "No dual-source available; requires expedited spot vendor onboarding.",
            "expected_benefit": "Secures secondary raw material pipeline and mitigates single-source dependency."
        },
        {
            "priority": "HIGH",
            "action": f"Re-sequence {len(pids)} downstream stages ({', '.join(pids[:2])}) for non-{supplier['material']} recipes",
            "reason": f"Prevents idle chamber starvation while {supplier['material']} shipments are delayed.",
            "expected_benefit": "Maintains overall fab equipment utilization and protects SLA commitments."
        }
    ]

    return {
        "scenario": "Supplier Disruption",
        "scenario_name": "Supplier Disruption",
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
            "risk_score": base_risk["supplier_risk_score"],
            "risk_level": base_risk["risk_level"],
            "predicted_delay_hours": baseline_avg_delay,
            "total_delay_hours": baseline_avg_delay,
            "affected_lots_count": 0,
            "affected_lots": 0,
            "wafers_at_risk": 0,
            "business_exposure_usd": 0.0
        },
        "simulated": {
            "supplier_risk_score": sim_risk["supplier_risk_score"],
            "risk_score": sim_risk["supplier_risk_score"],
            "risk_level": "CRITICAL",
            "predicted_delay_hours": simulated_total_delay_hr,
            "total_delay_hours": simulated_total_delay_hr,
            "affected_lots_count": len(affected_lots),
            "affected_lots": len(affected_lots),
            "wafers_at_risk": total_wafers,
            "business_exposure_usd": business_exposure_usd
        },
        "delta": {
            "risk_score_diff": round(sim_risk["supplier_risk_score"] - base_risk["supplier_risk_score"], 1),
            "risk_score_delta": round(sim_risk["supplier_risk_score"] - base_risk["supplier_risk_score"], 1),
            "delay_increase_hours": simulated_additional_delay_hr,
            "delay_hours_delta": simulated_additional_delay_hr,
            "lots_affected_diff": len(affected_lots),
            "affected_lots_delta": len(affected_lots),
            "exposure_increase_usd": business_exposure_usd
        },
        "financial_impact_millions": financial_impact_millions,
        "affected_processes": pids,
        "operational_impact_summary": operational_impact_summary,
        "mitigation_recommendation": {
            "action": primary_action,
            "detail": primary_detail,
            "priority": "CRITICAL"
        },
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
    total_lot_value = sum(l["lot_value_usd"] for l in lots)
    
    # Baseline metrics
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
    
    simulated_delay = round(pred["predicted_delay_hours"] + (failure_duration_hours * 0.85), 1)
    baseline_delay = 6.5
    delay_delta = round(simulated_delay - baseline_delay, 1)
    
    business_exposure_usd = round(total_lot_value * min(1.0, (failure_duration_hours / 72.0) * 0.35), 2)
    financial_impact_millions = round(max(0.6, business_exposure_usd / 1_000_000.0), 2)

    # Intelligent Scenario-Specific Primary Mitigation
    if alt_tool_names:
        primary_action = f"Reroute {len(lots)} queued lots from {tool_id} to qualified alternate tools ({', '.join(alt_tool_names)})"
    else:
        primary_action = f"Dispatch emergency field service on single-source tool {tool_id} and pause upstream WIP feed"

    primary_detail = (
        f"An unscheduled {failure_duration_hours}h outage on {tool_id} ({tool['name']}) halts stage {tool['process_id']}, "
        f"accumulating {simulated_wip} WIP lots (+{simulated_wip - tool['current_wip']}) and adding +{delay_delta:.1f}h delay "
        f"to {len(lots)} lots ({total_wafers:,} wafers) with ${financial_impact_millions}M exposure."
    )

    operational_impact_summary = (
        f"Unscheduled breakdown of {tool_id} ({tool['name']}) for {failure_duration_hours} hours halts {tool['process_id']}. "
        f"Active WIP queue increases from {tool['current_wip']} to {simulated_wip} lots ({total_wafers:,} wafers), "
        f"pushing utilization to 250% (CRITICAL) and risking downstream process line starvation."
    )

    # Prioritized Supporting Actions
    recommendations = [
        {
            "priority": "CRITICAL",
            "action": f"Reallocate incoming lots to alternate tools: {', '.join(alt_tool_names) if alt_tool_names else 'Single-source tool — dispatch emergency repair team'}",
            "reason": f"{tool_id} outage of {failure_duration_hours}h stops processing of {len(lots)} queued lots.",
            "expected_benefit": f"Absorbs queue congestion across {'parallel chambers' if alt_tool_names else 'urgent maintenance'} and reduces delay by ~60%."
        },
        {
            "priority": "HIGH",
            "action": f"Prioritize {high_priority_count} critical/high priority lots for immediate recovery dispatch",
            "reason": f"{high_priority_count} high-priority lots in {tool_id} queue carry urgent customer SLA delivery milestones.",
            "expected_benefit": "Prevents late delivery penalties on tier-1 semiconductor accounts."
        },
        {
            "priority": "MEDIUM",
            "action": f"Hold upstream lot dispatch from preceding process stage to {tool['process_id']}",
            "reason": f"Prevents excessive buffer pileup in front of unavailable {tool_id}.",
            "expected_benefit": "Stabilizes line equilibrium and prevents wafer staging congestion."
        }
    ]

    return {
        "scenario": "Equipment Failure",
        "scenario_name": "Equipment Outage",
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
            "predicted_delay_hours": baseline_delay,
            "total_delay_hours": baseline_delay,
            "affected_lots_count": len(lots),
            "affected_lots": len(lots)
        },
        "simulated": {
            "utilization_pct": 250.0,
            "risk_level": "CRITICAL",
            "risk_score": 98.5,
            "current_wip": simulated_wip,
            "predicted_delay_hours": simulated_delay,
            "total_delay_hours": simulated_delay,
            "affected_lots_count": len(lots) + 6,
            "affected_lots": len(lots) + 6
        },
        "delta": {
            "delay_increase_hours": delay_delta,
            "delay_hours_delta": delay_delta,
            "wip_increase": simulated_wip - tool["current_wip"],
            "lots_affected_diff": 6,
            "affected_lots_delta": 6,
            "risk_score_diff": round(98.5 - base_metrics["risk_score"], 1),
            "risk_score_delta": round(98.5 - base_metrics["risk_score"], 1)
        },
        "financial_impact_millions": financial_impact_millions,
        "alternate_tools": alt_tool_names,
        "operational_impact_summary": operational_impact_summary,
        "mitigation_recommendation": {
            "action": primary_action,
            "detail": primary_detail,
            "priority": "CRITICAL"
        },
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
    total_wafers = sum(l["wafer_quantity"] for l in lots)
    high_priority_count = sum(1 for l in lots if l["priority"] in ("HIGH", "CRITICAL"))
    total_lot_value = sum(l["lot_value_usd"] for l in lots)
    
    base_metrics = calculate_bottleneck_metrics(tool["nominal_capacity"], tool["current_wip"], tool_id, len(lots))
    
    # Reduced capacity calculation
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

    baseline_delay = 3.8
    simulated_delay = round(pred["predicted_delay_hours"], 1)
    delay_delta = round(simulated_delay - baseline_delay, 1)
    capacity_loss = tool["nominal_capacity"] - derated_capacity
    utilization_increase_pct = round(sim_metrics["utilization_pct"] - base_metrics["utilization_pct"], 1)
    
    business_exposure_usd = round(total_lot_value * min(1.0, (reduction_pct / 100.0) * (duration_days / 14.0) * 0.25), 2)
    financial_impact_millions = round(max(0.3, business_exposure_usd / 1_000_000.0), 2)

    # Intelligent Scenario-Specific Primary Mitigation
    primary_action = f"Rebalance stage {tool['process_id']} chamber loading and shift non-urgent {tool_id} lots to off-peak shifts"
    primary_detail = (
        f"A {reduction_pct:.0f}% capacity derating on {tool_id} ({derated_capacity} vs {tool['nominal_capacity']} nominal wpd) "
        f"pushes utilization to {sim_metrics['utilization_pct']:.1f}% ({sim_metrics['risk_level']}), increasing average cycle delay "
        f"by +{delay_delta:+.1f}h across {len(lots)} lots over {duration_days} days."
    )

    operational_impact_summary = (
        f"Derating {tool_id} ({tool['name']}) by {reduction_pct:.0f}% for {duration_days} days reduces daily throughput by {capacity_loss} wafers/day. "
        f"Queue utilization jumps from {base_metrics['utilization_pct']:.1f}% to {sim_metrics['utilization_pct']:.1f}%, raising risk level to "
        f"{sim_metrics['risk_level']} with +{delay_delta:.1f}h projected delay drift across {total_wafers:,} wafers."
    )

    # Prioritized Supporting Actions
    recommendations = [
        {
            "priority": "HIGH" if sim_metrics["risk_level"] in ("CRITICAL", "HIGH") else "MEDIUM",
            "action": f"Shift batch schedules on {tool_id} to auxiliary/night shifts",
            "reason": f"Capacity derated by {reduction_pct:.0f}%, pushing utilization to {sim_metrics['utilization_pct']:.1f}%.",
            "expected_benefit": f"Absorbs queue accumulation and recovers ~{capacity_loss * duration_days} wafers of lost fab throughput."
        },
        {
            "priority": "HIGH",
            "action": f"Fast-track {high_priority_count} high-priority lots ahead of standard production lots in {tool_id} queue",
            "reason": f"Derated capacity creates cycle-time slip for non-expedited wafer batches.",
            "expected_benefit": "Ensures on-time delivery commitments for Tier-1 customer orders."
        },
        {
            "priority": "MEDIUM",
            "action": f"Re-route compatible recipe steps to parallel tools in stage {tool['process_id']}",
            "reason": f"Alleviates the {utilization_increase_pct:+.1f}% utilization surge on {tool_id}.",
            "expected_benefit": "Restores balanced utilization across the stage equipment fleet."
        }
    ]

    return {
        "scenario": "Capacity Reduction",
        "scenario_name": "Capacity Loss",
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
            "predicted_delay_hours": baseline_delay,
            "total_delay_hours": baseline_delay,
            "affected_lots_count": len(lots),
            "affected_lots": len(lots)
        },
        "simulated": {
            "nominal_capacity": derated_capacity,
            "utilization_pct": sim_metrics["utilization_pct"],
            "risk_level": sim_metrics["risk_level"],
            "risk_score": sim_metrics["risk_score"],
            "predicted_delay_hours": simulated_delay,
            "total_delay_hours": simulated_delay,
            "affected_lots_count": len(lots) + max(1, int(reduction_pct / 15)),
            "affected_lots": len(lots) + max(1, int(reduction_pct / 15))
        },
        "delta": {
            "capacity_loss": capacity_loss,
            "utilization_increase_pct": utilization_increase_pct,
            "delay_increase_hours": delay_delta,
            "delay_hours_delta": delay_delta,
            "risk_score_diff": round(sim_metrics["risk_score"] - base_metrics["risk_score"], 1),
            "risk_score_delta": round(sim_metrics["risk_score"] - base_metrics["risk_score"], 1),
            "lots_affected_diff": max(1, int(reduction_pct / 15)),
            "affected_lots_delta": max(1, int(reduction_pct / 15))
        },
        "financial_impact_millions": financial_impact_millions,
        "operational_impact_summary": operational_impact_summary,
        "mitigation_recommendation": {
            "action": primary_action,
            "detail": primary_detail,
            "priority": "HIGH"
        },
        "recommended_actions": recommendations
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
    delay_delta = round(avg_sim_delay - avg_base_delay, 1)
    additional_bottlenecks = max(0, simulated_critical_count - baseline_critical_count)
    
    financial_impact_millions = round(max(0.5, (demand_increase_pct / 100.0) * 2.2 + (delay_delta * 0.12)), 2)

    # Intelligent Scenario-Specific Primary Mitigation
    primary_action = f"Activate dynamic priority dispatch rules and reserve dedicated tool capacity for +{demand_increase_pct:.0f}% volume surge"
    primary_detail = (
        f"A +{demand_increase_pct:.0f}% wafer demand surge over {duration_weeks} weeks pushes {simulated_critical_count} fab tools "
        f"into high/critical bottleneck state (+{additional_bottlenecks} new bottlenecks), increasing average lot delay from "
        f"{avg_base_delay:.1f}h to {avg_sim_delay:.1f}h (+{delay_delta:+.1f}h) across the active fleet."
    )

    operational_impact_summary = (
        f"Incoming demand spike of +{demand_increase_pct:.0f}% across {duration_weeks} weeks increases WIP queue pressure line-wide, "
        f"converting {additional_bottlenecks} additional equipment tools into critical bottlenecks. Average lot delivery delay increases "
        f"by +{delay_delta:.1f}h, shifting fab status to {('OVERBURDENED' if simulated_critical_count > baseline_critical_count + 3 else 'ELEVATED')}."
    )

    # Prioritized Supporting Actions
    recommendations = [
        {
            "priority": "HIGH",
            "action": f"Implement dynamic dispatch prioritizing Tier-1 committed lots over standard runs",
            "reason": f"A {demand_increase_pct:.0f}% volume surge creates competing queue pressure on {simulated_critical_count} constrained tools.",
            "expected_benefit": "Protects contractual SLA commitments while maximizing fab revenue."
        },
        {
            "priority": "HIGH",
            "action": f"Scale raw consumable orders (photoresist, CMP slurry, precursor gases) by +{demand_increase_pct:.0f}%",
            "reason": "Consumables burn rate accelerates proportionally with the higher wafer starts.",
            "expected_benefit": "Prevents upstream stockouts during the elevated production run rate."
        },
        {
            "priority": "MEDIUM",
            "action": f"Authorize weekend auxiliary operating shifts on the {simulated_critical_count} bottleneck tools",
            "reason": f"Absorbs the {additional_bottlenecks} newly formed bottlenecks without adding fixed tooling capex.",
            "expected_benefit": "Restores nominal line balance and keeps average delay within 6 hours."
        }
    ]

    base_risk = 72.0
    sim_risk = min(99.0, round(base_risk + demand_increase_pct * 0.45, 1))

    return {
        "scenario": "Demand Surge",
        "scenario_name": "Demand Surge",
        "scenario_type": "DEMAND_INCREASE",
        "parameters": {
            "demand_increase_pct": demand_increase_pct,
            "duration_weeks": duration_weeks
        },
        "baseline": {
            "critical_bottlenecks_count": baseline_critical_count,
            "average_predicted_delay_hours": avg_base_delay,
            "total_delay_hours": avg_base_delay,
            "predicted_delay_hours": avg_base_delay,
            "risk_score": base_risk,
            "affected_lots": 24,
            "affected_lots_count": 24,
            "fab_capacity_status": "MANAGEABLE"
        },
        "simulated": {
            "critical_bottlenecks_count": simulated_critical_count,
            "average_predicted_delay_hours": avg_sim_delay,
            "total_delay_hours": avg_sim_delay,
            "predicted_delay_hours": avg_sim_delay,
            "risk_score": sim_risk,
            "affected_lots": 24 + int(demand_increase_pct * 0.6),
            "affected_lots_count": 24 + int(demand_increase_pct * 0.6),
            "fab_capacity_status": "OVERBURDENED" if simulated_critical_count > baseline_critical_count + 3 else "ELEVATED"
        },
        "delta": {
            "additional_bottleneck_tools": additional_bottlenecks,
            "delay_increase_hours": delay_delta,
            "delay_hours_delta": delay_delta,
            "risk_score_diff": round(sim_risk - base_risk, 1),
            "risk_score_delta": round(sim_risk - base_risk, 1),
            "lots_affected_diff": int(demand_increase_pct * 0.6),
            "affected_lots_delta": int(demand_increase_pct * 0.6)
        },
        "financial_impact_millions": financial_impact_millions,
        "operational_impact_summary": operational_impact_summary,
        "mitigation_recommendation": {
            "action": primary_action,
            "detail": primary_detail,
            "priority": "HIGH"
        },
        "recommended_actions": recommendations
    }
