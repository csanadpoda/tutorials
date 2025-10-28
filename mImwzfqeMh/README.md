# Weather Metrics Service

A minimal FastAPI + SQLAlchemy application for collecting and querying weather sensor data.

---

## Overview

This service receives metric readings (temperature, humidity, wind speed, etc.) from weather sensors and provides query endpoints for statistics such as **min**, **max**, **sum**, and **average** over configurable date ranges.

---

## Features

- REST API built with **FastAPI**
- ORM and database abstraction via **SQLAlchemy**
- Flexible storage backend (SQLite by default, PostgreSQL compatible)
- Input validation and schema management with **Pydantic**
- Unit/integration tests via **pytest**
- Configurable via `.env` file

---

## Setup

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (preferred) or `pip`

### Installation

```bash
# Install dependencies
uv sync

# Run migrations / create schema
uv run python -m app.main
```

---

## Running the Application

```bash
uv run uvicorn app.main:app --reload
```

The server starts on `http://127.0.0.1:8000`.

OpenAPI documentation:
- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## Configuration

Environment variables are read from `.env` (requires `python-dotenv`).

Example:

```bash
DATABASE_URL=sqlite:///weather.db
# DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/weather
```

---

## Testing

```bash
uv run pytest -q
```

Tests are isolated with a temporary SQLite database.  
All tests are self-contained and automatically clean up after execution.

---

## API Summary

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/sensors` | Register a new sensor |
| POST | `/readings` | Record a new reading |
| POST | `/metrics/query` | Query statistics for one or more sensors |
| GET  | `/healthz` | Health check endpoint |

### Example Query

```json
{
  "sensor_ids": [1],
  "metrics": ["temperature", "humidity"],
  "stat": "avg",
  "start": "2025-10-20T00:00:00Z",
  "end": "2025-10-27T23:59:59Z"
}
```

---

## Directory Structure

```
app/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── stats.py
tests/
└── test_api.py
```

---

## Development Notes

- The ORM model defines two tables: `sensors` and `readings`.
- Each reading is stored row-wise (`sensor_id`, `metric`, `value`, `recorded_at`).
- Aggregations are computed using SQLAlchemy’s `func` abstraction.

---

## TODO / Extensions

- [ ] Batch ingestion endpoint for multiple readings
- [ ] Percentile and median statistics
- [ ] Query bucketing (hourly, daily averages)
- [ ] Authentication / API keys
- [ ] Rate limiting
- [ ] Add Prometheus metrics for observability
- [ ] Switch to Postgres if concurrency/scalability is needed