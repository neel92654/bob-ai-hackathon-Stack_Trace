"""
Nexora — Production Lot Impact & Delivery Prediction REST API
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

from flask import Blueprint, jsonify, request
from src.backend.services.delivery_prediction_service import (
    get_production_lots_impact,
    get_lot_by_id
)

production_bp = Blueprint("production", __name__)

@production_bp.route("/lots", methods=["GET"])
def list_lots():
    """
    Returns production lots with ML-predicted delays, urgency rankings, and filter support.
    """
    try:
        pri = request.args.get("priority")
        proc = request.args.get("process")
        tool = request.args.get("tool")
        data = get_production_lots_impact(filter_priority=pri, filter_process=proc, filter_tool=tool)
        return jsonify({
            "status": "success",
            "summary": data["summary"],
            "count": len(data["lots"]),
            "data": data["lots"]
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@production_bp.route("/lots/<lot_id>", methods=["GET"])
def get_lot_details(lot_id):
    """
    Returns detailed delay impact for a single production lot.
    """
    try:
        lot = get_lot_by_id(lot_id.upper())
        if not lot:
            return jsonify({"status": "error", "message": f"Lot '{lot_id}' not found."}), 404
        return jsonify({
            "status": "success",
            "data": lot
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
