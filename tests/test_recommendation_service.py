"""
Nexora — Prioritized Recommendation Engine Tests
"""

import pytest
from src.backend.services.recommendation_service import generate_recommendations

def test_generate_recommendations_populated():
    res = generate_recommendations()
    assert res["total_recommendations"] > 0
    assert len(res["recommendations"]) > 0
    assert res["critical_count"] > 0
    
    # Check structure of each recommendation
    for rec in res["recommendations"]:
        assert "id" in rec
        assert "priority" in rec
        assert "action" in rec
        assert "reason" in rec
        assert "expected_benefit" in rec
        assert rec["priority"] in ("CRITICAL", "HIGH", "MEDIUM", "LOW")

def test_recommendation_filtering():
    crit_recs = generate_recommendations(priority_filter="CRITICAL")
    assert all(r["priority"] == "CRITICAL" for r in crit_recs["recommendations"])
