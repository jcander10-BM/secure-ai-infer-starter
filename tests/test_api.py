import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("API_KEY", "demo")

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
    for k in ("label", "score", "request_id"):
        assert k in body
