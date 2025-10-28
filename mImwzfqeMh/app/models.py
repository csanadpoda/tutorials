from __future__ import annotations
from datetime import datetime, UTC
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Sensor(Base):
    __tablename__ = "sensors"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), unique=True, nullable=False)
    location = Column(String(256), nullable=True)
    created_at = Column(DateTime, default=datetime.now(UTC), nullable=False)

    readings = relationship("Reading", back_populates="sensor", cascade="all, delete-orphan")

class Reading(Base):
    __tablename__ = "readings"
    id = Column(Integer, primary_key=True, autoincrement=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False, index=True)
    metric = Column(String(64), nullable=False, index=True)
    value = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.now(UTC), nullable=False, index=True)

    sensor = relationship("Sensor", back_populates="readings")

Index(
    "ix_readings_sensor_metric_time",
    Reading.sensor_id,
    Reading.metric,
    Reading.recorded_at,
)