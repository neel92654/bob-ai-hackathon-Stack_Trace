"""
Nexora — Full REST API Integration Tests & Error Handling
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

import json
import pytest

def test_api_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"
    assert data["database_connected"] is True
    assert data["ml_model_loaded"] is True
    assert "problem_statement" in data

def test_api_dashboard_summary(client):
    response = client.get("/api/dashboard/summary")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "kpi_metrics" in data
    assert "distributions" in data
    assert "critical_alerts" in data
    assert data["kpi_metrics"]["overall_operational_risk_score"] > 0

def test_api_bottlenecks_list(client):
    response = client.get("/api/bottlenecks")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["count"] >= 20

def test_api_bottleneck_details_valid(client):
    response = client.get("/api/bottlenecks/CVD-03")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"]["tool_id"] == "CVD-03"
    assert "assigned_lots" in data["data"]

def test_api_bottleneck_details_not_found(client):
    response = client.get("/api/bottlenecks/NON_EXISTENT_TOOL")
    assert response.status_code == 404
    data = response.get_json()
    assert data["status"] == "error"

def test_api_suppliers_list(client):
    response = client.get("/api/suppliers")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["count"] >= 20

def test_api_supplier_details_valid(client):
    response = client.get("/api/suppliers/SUP-002")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"]["supplier_id"] == "SUP-002"
    assert data["data"]["is_single_point_of_failure"] is True

def test_api_supplier_details_not_found(client):
    response = client.get("/api/suppliers/SUP_INVALID_999")
    assert response.status_code == 404
    data = response.get_json()
    assert data["status"] == "error"

def test_api_geopolitical_concentration(client):
    response = client.get("/api/suppliers/geopolitical-concentration")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert len(data["data"]) > 0

def test_api_production_lots(client):
    response = client.get("/api/production/lots")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["count"] >= 100

def test_api_simulation_valid(client):
    payload = {
        "scenario_type": "SUPPLIER_DISRUPTION",
        "params": {
            "supplier_id": "SUP-002",
            "duration_days": 14
        }
    }
    response = client.post(
        "/api/simulation/run",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"]["scenario_type"] == "SUPPLIER_DISRUPTION"

def test_api_simulation_missing_type(client):
    response = client.post(
        "/api/simulation/run",
        data=json.dumps({"params": {}}),
        content_type="application/json"
    )
    assert response.status_code == 400
    data = response.get_json()
    assert data["status"] == "error"

def test_api_recommendations_list(client):
    response = client.get("/api/recommendations")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert data["data"]["total_recommendations"] > 0

def test_api_assistant_grounded_query(client):
    payload = {"query": "Why is CVD-03 critical?"}
    response = client.post(
        "/api/assistant/query",
        data=json.dumps(payload),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "CVD-03" in data["data"]["direct_answer"]
    assert len(data["data"]["supporting_facts"]) > 0

def test_api_assistant_empty_query(client):
    response = client.post(
        "/api/assistant/query",
        data=json.dumps({"query": ""}),
        content_type="application/json"
    )
    assert response.status_code == 400
