"""
Nexora — Fab Bottleneck REST API
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

from flask import Blueprint, jsonify
from src.backend.services.bottleneck_service import get_all_bottlenecks, get_bottleneck_by_id

bottleneck_bp = Blueprint("bottlenecks", __name__)

@bottleneck_bp.route("", methods=["GET"])
def list_bottlenecks():
    """
    Returns list of all fab tools with utilization, queue pressure, risk level, and explanations.
    """
    try:
        bottlenecks = get_all_bottlenecks()
        return jsonify({
            "status": "success",
            "count": len(bottlenecks),
            "data": bottlenecks
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@bottleneck_bp.route("/<tool_id>", methods=["GET"])
def get_bottleneck_details(tool_id):
    """
    Returns specific tool bottleneck analytics, assigned lots, and process stage flow.
    """
    try:
        tool = get_bottleneck_by_id(tool_id.upper())
        if not tool:
            return jsonify({"status": "error", "message": f"Equipment '{tool_id}' not found."}), 404
        return jsonify({
            "status": "success",
            "data": tool
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
