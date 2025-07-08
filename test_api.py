import os
import json
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
LOG_PATH = os.path.join(os.path.dirname(__file__), 'logs', 'log.jsonl')


def clear_log():
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)


def read_log():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, 'r') as f:
        return [json.loads(line) for line in f if line.strip()]


def test_generate_success():
    clear_log()
    prompt = "Test prompt"
    response = client.post("/generate", json={"prompt": prompt})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert prompt in data["response"]

    # Check log
    logs = read_log()
    assert len(logs) == 1
    assert logs[0]["prompt"] == prompt
    assert prompt in logs[0]["response"]


def test_generate_empty_prompt():
    clear_log()
    response = client.post("/generate", json={"prompt": ""})
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert data["response"] == "Stubbed response for: ''"
    logs = read_log()
    assert len(logs) == 1
    assert logs[0]["prompt"] == ""


def test_generate_missing_prompt():
    clear_log()
    response = client.post("/generate", json={})
    assert response.status_code == 422  # Unprocessable Entity
    logs = read_log()
    assert len(logs) == 0


def test_generate_invalid_json():
    clear_log()
    response = client.post("/generate", data="not a json",
                           headers={"Content-Type": "application/json"})
    assert response.status_code == 422
    logs = read_log()
    assert len(logs) == 0
