"""
Nexora — Operational Risk & Supply Intelligence Platform Backend
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)

Main Flask Application Entry Point & API Gateway.
"""

import os
import sys
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.backend.config.settings import APP_PORT, DEBUG, DB_PATH
from src.backend.routes.dashboard_routes import dashboard_bp
from src.backend.routes.bottleneck_routes import bottleneck_bp
from src.backend.routes.supplier_routes import supplier_bp
from src.backend.routes.production_routes import production_bp
from src.backend.routes.simulation_routes import simulation_bp
from src.backend.routes.recommendation_routes import recommendation_bp
from src.backend.routes.assistant_routes import assistant_bp
from src.backend.ml.predict_delivery import load_model

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register API Blueprints
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(bottleneck_bp, url_prefix="/api/bottlenecks")
    app.register_blueprint(supplier_bp, url_prefix="/api/suppliers")
    app.register_blueprint(production_bp, url_prefix="/api/production")
    app.register_blueprint(simulation_bp, url_prefix="/api/simulation")
    app.register_blueprint(recommendation_bp, url_prefix="/api/recommendations")
    app.register_blueprint(assistant_bp, url_prefix="/api/assistant")

    @app.route("/api/health", methods=["GET"])
    def health_check():
        db_exists = os.path.exists(DB_PATH)
        model, metadata = load_model()
        model_loaded = model is not None

        return jsonify({
            "status": "healthy",
            "service": "Nexora Operational Risk & Supply Intelligence API",
            "version": "1.0.0",
            "hackathon": "IBM Bob AI Innovation Hackathon 2026",
            "problem_statement": "S2 — Fab Bottleneck & Supply Chain Risk Advisor",
            "database_connected": db_exists,
            "ml_model_loaded": model_loaded,
            "ml_metrics": metadata.get("metrics", {}) if metadata else {},
            "dataset_nature": "Synthetic demonstration dataset (reproducible seed 42)",
            "timestamp": datetime.now().isoformat()
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"status": "error", "message": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"status": "error", "message": "Internal server error"}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    print("=" * 60)
    print(f"Starting Nexora Backend API Server on port {APP_PORT}...")
    print(f"Health check: http://127.0.0.1:{APP_PORT}/api/health")
    print("=" * 60)
    app.run(host="0.0.0.0", port=APP_PORT, debug=DEBUG)
