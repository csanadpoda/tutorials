import os
import tempfile
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, UTC

fd, path = tempfile.mkstemp(suffix=".db")
os.close(fd)
os.environ["DATABASE_URL"] = f"sqlite:///{path}"

from app.main import app
from app.models import Base
from app.database import engine

Base.metadata.create_all(bind=engine)
client = TestClient(app)


@pytest.fixture(scope="session", autouse=True)
def cleanup_db():
    yield
    try:
        os.remove(path)
    except FileNotFoundError:
        pass


def test_ingest_and_query_avg():
    r = client.post("/sensors", json={"name": "sensor-1", "location": "lab"})
    assert r.status_code == 200
    sid = r.json()["id"]

    now = datetime.now(UTC)
    payloads = [
        {"sensor_id": sid, "metric": "temperature", "value": 20.0, "recorded_at": (now - timedelta(hours=2)).isoformat()},
        {"sensor_id": sid, "metric": "temperature", "value": 22.0, "recorded_at": (now - timedelta(hours=1)).isoformat()},
        {"sensor_id": sid, "metric": "humidity", "value": 40.0, "recorded_at": (now - timedelta(hours=1, minutes=30)).isoformat()},
    ]
    for p in payloads:
        rr = client.post("/readings", json=p)
        assert rr.status_code == 200

    q = {
        "sensor_ids": [sid],
        "metrics": ["temperature", "humidity"],
        "stat": "avg",
        "start": (now - timedelta(days=1)).isoformat(),
        "end": now.isoformat(),
    }
    qr = client.post("/metrics/query", json=q)
    assert qr.status_code == 200
    data = qr.json()
    results = {(r["metric"], r["sensor_id"]): r["value"] for r in data["results"]}
    assert round(results[("temperature", sid)], 3) == 21.0
    assert round(results[("humidity", sid)], 3) == 40.0


def test_range_validation():
    r = client.post("/metrics/query", json={
        "metrics": ["temperature"],
        "stat": "avg",
        "start": (datetime.now(UTC) - timedelta(hours=1)).isoformat(),
        "end": datetime.now(UTC).isoformat(),
    })
    assert r.status_code == 422
    assert "at least 1 day" in r.json()["detail"]


def test_unknown_sensor_reading_rejected():
    r = client.post("/readings", json={"sensor_id": 9999, "metric": "t", "value": 1.0})
    assert r.status_code == 404


def test_duplicate_sensor_name_rejected():
    client.post("/sensors", json={"name": "dup", "location": "a"})
    r = client.post("/sensors", json={"name": "dup", "location": "b"})
    assert r.status_code == 409


def test_reading_missing_metric_field():
    r = client.post("/readings", json={"sensor_id": 1, "value": 10})
    assert r.status_code == 422


def test_query_all_sensors():
    r = client.post("/metrics/query", json={
        "metrics": ["temperature"],
        "stat": "avg",
        "start": (datetime.now(UTC) - timedelta(days=1)).isoformat(),
        "end": datetime.now(UTC).isoformat(),
    })
    assert r.status_code == 200
    assert "results" in r.json()


def test_query_invalid_stat():
    r = client.post("/metrics/query", json={
        "metrics": ["temperature"],
        "stat": "median",
        "start": (datetime.now(UTC) - timedelta(days=1)).isoformat(),
        "end": datetime.now(UTC).isoformat(),
    })
    assert r.status_code == 422


def test_query_date_window_too_long():
    r = client.post("/metrics/query", json={
        "metrics": ["temperature"],
        "stat": "avg",
        "start": (datetime.now(UTC) - timedelta(days=32)).isoformat(),
        "end": datetime.now(UTC).isoformat(),
    })
    assert r.status_code == 422


def test_health_endpoint():
    r = client.get("/healthz")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}