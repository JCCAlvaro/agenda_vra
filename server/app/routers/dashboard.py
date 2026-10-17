from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import current_user
from ..models import Actividad, Usuario
from ..schemas import _serialize_dt

router = APIRouter(prefix="/dashboard", tags=["dashboard"])
LIMA = ZoneInfo("America/Lima")


@router.get("")
def dashboard(db: Session = Depends(get_db), user: Usuario = Depends(current_user)):
    now_lima = datetime.now(LIMA)
    start_lima = now_lima.replace(hour=0, minute=0, second=0, microsecond=0)
    end_lima = start_lima + timedelta(days=1)
    week_end_lima = start_lima + timedelta(days=7)

    start = start_lima.astimezone(timezone.utc).replace(tzinfo=None)
    end = end_lima.astimezone(timezone.utc).replace(tzinfo=None)
    week_end = week_end_lima.astimezone(timezone.utc).replace(tzinfo=None)
    now_utc = datetime.now(timezone.utc).replace(tzinfo=None)

    hoy_q = (
        db.query(Actividad.prioridad, func.count(Actividad.id))
        .filter(Actividad.inicio >= start, Actividad.inicio < end)
        .filter(~Actividad.estado.in_(["cancelada", "completada"]))
        .group_by(Actividad.prioridad)
        .all()
    )
    hoy = {p: n for p, n in hoy_q}

    proximas = (
        db.query(Actividad)
        .filter(Actividad.inicio >= now_utc)
        .filter(~Actividad.estado.in_(["cancelada", "completada"]))
        .order_by(Actividad.inicio)
        .limit(5)
        .all()
    )

    semana_total = (
        db.query(func.count(Actividad.id))
        .filter(Actividad.inicio >= start, Actividad.inicio < week_end)
        .scalar()
    )

    return {
        "hoy": hoy,
        "proximas": [
            {
                "id": a.id,
                "titulo": a.titulo,
                "inicio": _serialize_dt(a.inicio),
                "prioridad": a.prioridad,
                "estado": a.estado,
            }
            for a in proximas
        ],
        "semana_total": semana_total,
    }