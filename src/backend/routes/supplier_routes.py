"""
Nexora — Supplier Risk & Geopolitical REST API
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

from flask import Blueprint, jsonify
from src.backend.services.supplier_risk_service import (
    get_all_suppliers_risk,
    get_supplier_by_id,
    get_geopolitical_summary
)

supplier_bp = Blueprint("suppliers", __name__)

@supplier_bp.route("", methods=["GET"])
def list_suppliers():
    """
    Returns list of all suppliers with explainable risk scores, factor breakdowns, and SPoF tags.
    """
    try:
        suppliers = get_all_suppliers_risk()
        return jsonify({
            "status": "success",
            "count": len(suppliers),
            "data": suppliers
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@supplier_bp.route("/<supplier_id>", methods=["GET"])
def get_supplier_details(supplier_id):
    """
    Returns single supplier profile, risk factor details, and affected production lots.
    """
    try:
        supplier = get_supplier_by_id(supplier_id.upper())
        if not supplier:
            return jsonify({"status": "error", "message": f"Supplier '{supplier_id}' not found."}), 404
        return jsonify({
            "status": "success",
            "data": supplier
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@supplier_bp.route("/geopolitical-concentration", methods=["GET"])
def get_geopolitical():
    """
    Returns country concentration analytics and critical material exposures.
    """
    try:
        geo = get_geopolitical_summary()
        return jsonify({
            "status": "success",
            "data": geo
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
