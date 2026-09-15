"""
Nexora — Grounded Decision Assistant REST API
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

from flask import Blueprint, jsonify, request
from src.backend.services.assistant_service import process_assistant_query

assistant_bp = Blueprint("assistant", __name__)

@assistant_bp.route("/query", methods=["POST"])
def query_assistant():
    """
    Processes natural-language queries grounded strictly in current Nexora fab and supply chain data.
    
    Expected JSON:
      { "query": "Why is CVD-03 critical?" }
    """
    try:
        body = request.get_json() or {}
        query_text = body.get("query", "")
        if not query_text:
            return jsonify({
                "status": "error",
                "message": "Query string is required in JSON body: {'query': '...'}"
            }), 400

        result = process_assistant_query(query_text)
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
