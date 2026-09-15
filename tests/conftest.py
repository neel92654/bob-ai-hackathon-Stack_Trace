"""
Nexora — Pytest Fixtures and Environment Setup
IBM Bob AI Innovation Hackathon 2026 (Problem Statement S2)
"""

import pytest
import os
import sys

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.backend.app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config.update({"TESTING": True})
    return app

@pytest.fixture
def client(app):
    return app.test_client()
