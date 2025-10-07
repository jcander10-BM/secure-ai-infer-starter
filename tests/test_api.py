import os, sys

# Ensure the app sees the expected key at import time
os.environ.setdefault("API_KEY", "demo")

# Make sure Python can import the package from repo root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the app module AFTER env is set (no reload!)
from app.api import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_predict_works():
    r = client.post(
        "/predict",
        headers={"X-API-Key": "demo", "Content-Type": "application/json"},
        json={"text": "reset your password"},
    )
    assert r.status_code == 200, f"Body: {r.text}"
    body = r.json()
    assert "label" in body and "score" in body and "request_id" in body


