"""
Nexora — Supplier Risk & Geopolitical Intelligence Service
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

from src.backend.models.database import query_db
from src.backend.utils.calculations import (
    calculate_supplier_risk_score,
    calculate_country_concentration
)

def get_all_suppliers_risk():
    """
    Retrieves all suppliers with explainable risk scores (0-100), SPoF flags,
    component weight breakdowns, and affected process names.
    """
    suppliers = query_db("SELECT * FROM suppliers ORDER BY supplier_id")
    routes = query_db("SELECT * FROM process_routes")
    route_map = {r["process_id"]: r["name"] for r in routes}
    
    results = []
    for s in suppliers:
        risk_data = calculate_supplier_risk_score(s)
        
        # Parse affected process IDs
        pids = [p.strip() for p in s["affected_process_ids"].split(",") if p.strip()]
        process_names = [route_map.get(pid, pid) for pid in pids]

        results.append({
            "supplier_id": s["supplier_id"],
            "name": s["name"],
            "material": s["material"],
            "country": s["country"],
            "lead_time_days": s["lead_time_days"],
            "dependency_pct": s["dependency_pct"],
            "criticality": s["criticality"],
            "alternate_supplier": s["alternate_supplier"],
            "alternate_lead_time_days": s["alternate_lead_time_days"],
            "alternate_capacity_pct": s["alternate_capacity_pct"],
            "geo_risk_factor": s["geo_risk_factor"],
            "status": s["status"],
            "is_single_point_of_failure": risk_data["is_single_point_of_failure"],
            "supplier_risk_score": risk_data["supplier_risk_score"],
            "risk_level": risk_data["risk_level"],
            "risk_reasons": risk_data["risk_reasons"],
            "factor_breakdown": risk_data["factor_breakdown"],
            "explanation": risk_data["explanation"],
            "affected_process_ids": pids,
            "affected_process_names": process_names
        })

    # Sort so SPoF and CRITICAL suppliers appear first
    severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
    results.sort(key=lambda x: (not x["is_single_point_of_failure"], severity_order.get(x["risk_level"], 4), -x["supplier_risk_score"]))
    return results

def get_supplier_by_id(supplier_id):
    """
    Retrieves detailed risk profile and affected fab processes for a single supplier.
    """
    all_suppliers = get_all_suppliers_risk()
    supplier = next((s for s in all_suppliers if s["supplier_id"] == supplier_id), None)
    if not supplier:
        return None
    
    # Identify affected lots currently in the affected process stages
    placeholders = ", ".join(["?"] * len(supplier["affected_process_ids"])) if supplier["affected_process_ids"] else "''"
    query = f"SELECT * FROM production_lots WHERE current_process_id IN ({placeholders})"
    affected_lots = query_db(query, supplier["affected_process_ids"])
    supplier["affected_lots"] = affected_lots
    supplier["affected_lots_count"] = len(affected_lots)
    supplier["affected_wafers_total"] = sum(l["wafer_quantity"] for l in affected_lots)

    return supplier

def get_geopolitical_summary():
    """
    Computes geographic concentration and country-level exposure from all suppliers.
    """
    all_suppliers = get_all_suppliers_risk()
    return calculate_country_concentration(all_suppliers)
