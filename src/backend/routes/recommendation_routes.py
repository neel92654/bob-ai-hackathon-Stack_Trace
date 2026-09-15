"""
Nexora — Prioritized Operational Recommendations REST API
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

from flask import Blueprint, jsonify, request
from src.backend.services.recommendation_service import generate_recommendations

recommendation_bp = Blueprint("recommendations", __name__)

@recommendation_bp.route("", methods=["GET"])
def list_recommendations():
    """
    Returns prioritized condition-driven recommendations with operational rationale.
    Supports optional ?category= and ?priority= query filters.
    """
    try:
        cat = request.args.get("category")
        pri = request.args.get("priority")
        result = generate_recommendations(category_filter=cat, priority_filter=pri)
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
