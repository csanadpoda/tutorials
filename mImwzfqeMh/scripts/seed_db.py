from app.database import session_scope
from app.models import Sensor, Reading
from datetime import datetime, UTC

with session_scope() as db:
    s = Sensor(name="sensor-demo", location="lab")
    db.add(s)
    db.flush()
    db.add_all([
        Reading(sensor_id=s.id, metric="temperature", value=21.5, recorded_at=datetime.now(UTC)),
        Reading(sensor_id=s.id, metric="humidity", value=45.2, recorded_at=datetime.now(UTC))
    ])