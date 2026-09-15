"""
Nexora — What-If Disruption Simulation REST API
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

from flask import Blueprint, jsonify, request
from src.backend.services.simulation_service import simulate_disruption

simulation_bp = Blueprint("simulation", __name__)

@simulation_bp.route("/run", methods=["POST"])
def run_simulation():
    """
    Executes a What-If operational disruption simulation.
    
    Expected JSON body:
      - scenario_type: "SUPPLIER_DISRUPTION" | "EQUIPMENT_FAILURE" | "CAPACITY_REDUCTION" | "DEMAND_INCREASE"
      - params: dict of scenario parameters
    """
    try:
        body = request.get_json() or {}
        scenario_type = body.get("scenario_type")
        params = body.get("params", {})
        
        if not scenario_type:
            return jsonify({
                "status": "error",
                "message": "Missing required field 'scenario_type'."
            }), 400

        result = simulate_disruption(scenario_type, params)
        return jsonify({
            "status": "success",
            "data": result
        })
    except ValueError as ve:
        return jsonify({"status": "error", "message": str(ve)}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": f"Simulation failed: {str(e)}"}), 500
