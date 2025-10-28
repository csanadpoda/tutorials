from __future__ import annotations
from datetime import datetime, timedelta, UTC
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ConfigDict

class StatEnum(str, Enum):
    min = "min"
    max = "max"
    sum = "sum"
    avg = "avg"

class SensorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    location: Optional[str] = Field(default=None, max_length=256)

class SensorOut(BaseModel):
    id: int
    name: str
    location: Optional[str]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class ReadingIn(BaseModel):
    sensor_id: int
    metric: str = Field(min_length=1, max_length=64)
    value: float
    recorded_at: Optional[datetime] = None

class ReadingOut(BaseModel):
    id: int
    sensor_id: int
    metric: str
    value: float
    recorded_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MetricsQuery(BaseModel):
    sensor_ids: Optional[List[int]] = None
    metrics: List[str]
    stat: StatEnum
    start: Optional[datetime] = None
    end: Optional[datetime] = None

    @field_validator("metrics")
    @classmethod
    def _nonempty_metrics(cls, v: List[str]):
        if not v:
            raise ValueError("metrics must not be empty")
        return v

    @field_validator("end")
    @classmethod
    def _end_after_start(cls, v: Optional[datetime], values):
        start = values.data.get("start")
        if start and v and v <= start:
            raise ValueError("end must be after start")
        return v

    def resolved_window(self) -> tuple[datetime, datetime]:
        if self.start and self.end:
            start, end = self.start, self.end
        else:
            end = datetime.now(UTC)
            start = end - timedelta(days=1)
        delta = end - start
        if delta < timedelta(days=1):
            raise ValueError("date range must be at least 1 day")
        if delta > timedelta(days=31):
            raise ValueError("date range must be at most 31 days")
        return start, end

class MetricStatResult(BaseModel):
    sensor_id: int
    metric: str
    stat: StatEnum
    value: float | None

class MetricsQueryResponse(BaseModel):
    start: datetime
    end: datetime
    stat: StatEnum
    results: List[MetricStatResult]