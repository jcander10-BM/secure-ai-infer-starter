from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)

def test_healthz():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_predict_auth_required():
    r = client.post("/predict", json={"text":"x"})
    assert r.status_code == 401

def test_predict_works():
    r = client.post("/predict", headers={"x-api-key":"demo"}, json={"text":"reset your password"})
    assert r.status_code == 200
    body = r.json()
    assert "label" in body and "score" in body and "request_id" in body
