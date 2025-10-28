from __future__ import annotations
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from .models import Reading
from .schemas import MetricsQuery, StatEnum

FUNC_MAP = {
    StatEnum.min: func.min,
    StatEnum.max: func.max,
    StatEnum.sum: func.sum,
    StatEnum.avg: func.avg,
}

def compute_stats(db: Session, q: MetricsQuery):
    start, end = q.resolved_window()

    agg_fn = FUNC_MAP[q.stat]
    stmt = (
        select(
            Reading.sensor_id.label("sensor_id"),
            Reading.metric.label("metric"),
            agg_fn(Reading.value).label("value"),
        )
        .where(Reading.recorded_at >= start, Reading.recorded_at <= end)
        .where(Reading.metric.in_(q.metrics))
        .group_by(Reading.sensor_id, Reading.metric)
    )

    if q.sensor_ids:
        stmt = stmt.where(Reading.sensor_id.in_(q.sensor_ids))

    rows = db.execute(stmt).all()

    requested_pairs = []
    if q.sensor_ids:
        for sid in q.sensor_ids:
            for m in q.metrics:
                requested_pairs.append((sid, m))
    else:
        requested_pairs = [(r.sensor_id, r.metric) for r in rows]

    values = {(r.sensor_id, r.metric): r.value for r in rows}

    return start, end, [
        {
            "sensor_id": sid,
            "metric": metric,
            "stat": q.stat,
            "value": float(values.get((sid, metric))) if values.get((sid, metric)) is not None else None,
        }
        for sid, metric in requested_pairs
    ]