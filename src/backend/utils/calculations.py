"""
Nexora — Analytics & Explainability Calculation Functions
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)

Provides pure, testable, deterministic calculations for fab bottleneck severity,
explainable supplier risk scoring, SPoF detection, and geopolitical concentration.
"""

from src.backend.config.settings import (
    BOTTLENECK_THRESHOLDS,
    SUPPLIER_RISK_WEIGHTS,
    SUPPLIER_RISK_THRESHOLDS
)

def calculate_bottleneck_metrics(nominal_capacity, current_wip, tool_id=None, affected_lot_count=0):
    """
    Computes capacity utilization, queue pressure, risk classification,
    and a clear natural-language explanation.
    """
    if nominal_capacity <= 0:
        utilization = 100.0
    else:
        utilization = (current_wip / nominal_capacity) * 100.0

    utilization = round(utilization, 1)
    queue_pressure = max(0, current_wip - nominal_capacity)

    # Classification
    if utilization < BOTTLENECK_THRESHOLDS["LOW"]:
        risk_level = "LOW"
        risk_score = min(25.0, round(utilization * 0.3, 1))
    elif utilization < BOTTLENECK_THRESHOLDS["MEDIUM"]:
        risk_level = "MEDIUM"
        risk_score = round(25.0 + ((utilization - 80.0) / 20.0) * 25.0, 1)
    elif utilization < BOTTLENECK_THRESHOLDS["HIGH"]:
        risk_level = "HIGH"
        risk_score = round(50.0 + ((utilization - 100.0) / 20.0) * 25.0, 1)
    else:
        risk_level = "CRITICAL"
        excess = min(60.0, utilization - 120.0)
        risk_score = min(100.0, round(75.0 + (excess / 60.0) * 25.0, 1))

    tool_label = tool_id or "This equipment"
    if risk_level == "CRITICAL":
        explanation = (
            f"{tool_label} is classified as CRITICAL because its WIP queue is {utilization:.0f}% of nominal "
            f"capacity ({current_wip} / {nominal_capacity} wafers) and it affects {affected_lot_count} active downstream lots."
        )
    elif risk_level == "HIGH":
        explanation = (
            f"{tool_label} is classified as HIGH risk because queue utilization is at {utilization:.0f}%, "
            f"operating above rated capacity by {queue_pressure} wafers."
        )
    elif risk_level == "MEDIUM":
        explanation = (
            f"{tool_label} is at MEDIUM risk with utilization at {utilization:.0f}%, approaching capacity limits."
        )
    else:
        explanation = (
            f"{tool_label} is operating within normal bounds at {utilization:.0f}% capacity utilization."
        )

    return {
        "nominal_capacity": nominal_capacity,
        "current_wip": current_wip,
        "utilization_pct": utilization,
        "queue_pressure": queue_pressure,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "explanation": explanation
    }

def calculate_supplier_risk_score(supplier_dict):
    """
    Computes explainable weighted supplier risk score (0-100) and factor breakdown.
    
    Formula:
      Supplier Risk Score = Dependency Risk + Lead Time Risk + Material Criticality +
                            Geographic Risk + Alternate Supplier Risk
    """
    dep_pct = float(supplier_dict.get("dependency_pct", 50))
    lead_time = float(supplier_dict.get("lead_time_days", 30))
    criticality = str(supplier_dict.get("criticality", "MEDIUM")).upper()
    geo_factor = float(supplier_dict.get("geo_risk_factor", 1.0))
    alternate = str(supplier_dict.get("alternate_supplier", "None"))
    alt_cap_pct = float(supplier_dict.get("alternate_capacity_pct", 0))

    # 1. Dependency Risk (0-100 scaled)
    comp_dep = dep_pct

    # 2. Lead Time Risk (60 days = 100)
    comp_lead = min(100.0, (lead_time / 60.0) * 100.0)

    # 3. Material Criticality
    crit_map = {"CRITICAL": 100.0, "HIGH": 75.0, "MEDIUM": 50.0, "LOW": 25.0}
    comp_crit = crit_map.get(criticality, 50.0)

    # 4. Geographic Risk (geo_factor: 1.0 -> 0, 2.0 -> 100)
    comp_geo = min(100.0, max(0.0, (geo_factor - 1.0) * 100.0))

    # 5. Alternate Supplier Risk
    if alternate in ("None", "none", "", None) or alt_cap_pct == 0:
        comp_alt = 100.0
    elif alt_cap_pct < 30:
        comp_alt = 70.0
    elif alt_cap_pct < 50:
        comp_alt = 40.0
    else:
        comp_alt = 15.0

    w = SUPPLIER_RISK_WEIGHTS
    raw_score = (
        comp_dep * w["dependency"] +
        comp_lead * w["lead_time"] +
        comp_crit * w["criticality"] +
        comp_geo * w["geographic_risk"] +
        comp_alt * w["alternate_avail"]
    )
    final_score = round(min(100.0, max(0.0, raw_score)), 1)

    # Risk level classification
    if final_score < SUPPLIER_RISK_THRESHOLDS["LOW"]:
        risk_level = "LOW"
    elif final_score < SUPPLIER_RISK_THRESHOLDS["MEDIUM"]:
        risk_level = "MEDIUM"
    elif final_score < SUPPLIER_RISK_THRESHOLDS["HIGH"]:
        risk_level = "HIGH"
    else:
        risk_level = "CRITICAL"

    # Single Point of Failure (SPoF) check
    is_spof = bool(
        (dep_pct >= 75 and (alternate in ("None", "none", "", None) or alt_cap_pct < 20)) or
        (criticality == "CRITICAL" and dep_pct >= 80 and comp_alt >= 70) or
        int(supplier_dict.get("single_point_of_failure", 0)) == 1
    )

    # Generate explainable reasons
    reasons = []
    if dep_pct >= 70:
        reasons.append(f"High market dependency ({int(dep_pct)}%)")
    if comp_crit >= 75:
        reasons.append(f"Material is rated {criticality} for production continuity")
    if comp_alt >= 70:
        reasons.append("No full secondary supplier qualified (zero or partial backup)")
    if lead_time >= 35:
        reasons.append(f"Extended procurement lead time ({int(lead_time)} days)")
    if comp_geo >= 50:
        reasons.append(f"High regional geopolitical exposure (Factor: {geo_factor}x)")

    if not reasons:
        reasons.append("Balanced multi-source supply with nominal lead time")

    explanation = (
        f"{supplier_dict.get('name', 'Supplier')} is rated {risk_level} (Score: {final_score}/100). "
        + " Key drivers: " + "; ".join(reasons) + "."
    )

    return {
        "supplier_risk_score": final_score,
        "risk_level": risk_level,
        "is_single_point_of_failure": is_spof,
        "factor_breakdown": {
            "dependency_component": round(comp_dep, 1),
            "lead_time_component": round(comp_lead, 1),
            "criticality_component": round(comp_crit, 1),
            "geographic_component": round(comp_geo, 1),
            "alternate_component": round(comp_alt, 1),
            "weights_used": SUPPLIER_RISK_WEIGHTS
        },
        "risk_reasons": reasons,
        "explanation": explanation
    }

def calculate_country_concentration(suppliers_list):
    """
    Groups suppliers by country and calculates country-level dependency share and critical material concentration.
    """
    country_map = {}
    for s in suppliers_list:
        c = s.get("country", "Unknown")
        if c not in country_map:
            country_map[c] = {
                "country": c,
                "supplier_count": 0,
                "suppliers": [],
                "materials": [],
                "total_dependency_sum": 0,
                "critical_materials": [],
                "has_spof": False
            }
        country_map[c]["supplier_count"] += 1
        country_map[c]["suppliers"].append(s.get("name"))
        country_map[c]["materials"].append(s.get("material"))
        country_map[c]["total_dependency_sum"] += float(s.get("dependency_pct", 0))
        if s.get("criticality") == "CRITICAL":
            country_map[c]["critical_materials"].append(s.get("material"))
        if s.get("is_single_point_of_failure") or int(s.get("single_point_of_failure", 0)) == 1:
            country_map[c]["has_spof"] = True

    results = []
    for c, data in country_map.items():
        avg_dep = round(data["total_dependency_sum"] / max(1, data["supplier_count"]), 1)
        # Concentration rating
        if len(data["critical_materials"]) >= 2 or (avg_dep >= 75 and data["supplier_count"] <= 2):
            concentration = "CRITICAL"
        elif avg_dep >= 55 or len(data["critical_materials"]) >= 1:
            concentration = "HIGH"
        elif avg_dep >= 35:
            concentration = "MEDIUM"
        else:
            concentration = "LOW"

        explanation = (
            f"{data['supplier_count']} supplier(s) located in {c} with average dependency of {avg_dep}%. "
            f"Critical materials sourced: {', '.join(data['critical_materials']) if data['critical_materials'] else 'None'}."
        )

        results.append({
            "country": c,
            "supplier_count": data["supplier_count"],
            "suppliers": data["suppliers"],
            "materials": data["materials"],
            "average_dependency_pct": avg_dep,
            "critical_materials": data["critical_materials"],
            "has_spof": data["has_spof"],
            "concentration_level": concentration,
            "explanation": explanation
        })

    return sorted(results, key=lambda x: (x["has_spof"], x["average_dependency_pct"]), reverse=True)
