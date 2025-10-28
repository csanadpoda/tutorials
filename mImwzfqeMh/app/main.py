from __future__ import annotations
from datetime import datetime, UTC
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import select
from .database import engine, session_scope
from .models import Base, Sensor, Reading
from .schemas import (
    SensorCreate, SensorOut,
    ReadingIn, ReadingOut,
    MetricsQuery, MetricsQueryResponse, MetricStatResult,
)
from .stats import compute_stats

app = FastAPI(title="weather-metrics-service", version="1.0.0")

Base.metadata.create_all(bind=engine)

@app.post("/sensors", response_model=SensorOut)
def create_sensor(payload: SensorCreate):
    with session_scope() as db:
        existing = db.execute(
            select(Sensor).where(Sensor.name == payload.name)
        ).scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=409, detail="sensor name already exists")

        s = Sensor(name=payload.name, location=payload.location)
        db.add(s)
        db.flush()
        db.refresh(s)
        result = SensorOut.model_validate(s, from_attributes=True)
    return result

@app.post("/readings", response_model=ReadingOut)
def ingest_reading(payload: ReadingIn):
    with session_scope() as db:
        sensor = db.get(Sensor, payload.sensor_id)
        if not sensor:
            raise HTTPException(status_code=404, detail="sensor not found")

        ts = payload.recorded_at or datetime.now(UTC)
        r = Reading(
            sensor_id=payload.sensor_id,
            metric=payload.metric,
            value=payload.value,
            recorded_at=ts,
        )
        db.add(r)
        db.flush()
        db.refresh(r)
        return ReadingOut.model_validate(r, from_attributes=True)
    
@app.post("/metrics/query", response_model=MetricsQueryResponse)
def metrics_query(q: MetricsQuery):
    try:
        with session_scope() as db:
            start, end, rows = compute_stats(db, q)
            results = [MetricStatResult(**row) for row in rows]
            return MetricsQueryResponse(start=start, end=end, stat=q.stat, results=results)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/healthz")
def health():
    return JSONResponse({"status": "ok"})