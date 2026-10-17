import logging
from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session

from .database import SessionLocal
from .models import Recordatorio, Actividad, Usuario

log = logging.getLogger("reminders")


def process_reminders():
    db: Session = SessionLocal()
    try:
        now_utc = datetime.now(timezone.utc).replace(tzinfo=None)
        rows = (
            db.query(Recordatorio)
            .filter(Recordatorio.enviado.is_(False))
            .filter(Recordatorio.enviar_en <= now_utc)
            .all()
        )
        for r in rows:
            act = db.query(Actividad).filter(Actividad.id == r.actividad_id).first()
            if not act or act.estado in ("cancelada", "completada"):
                continue
            usuario = db.query(Usuario).filter(Usuario.id == act.creado_por).first()
            # TODO: envío real por Gmail (ver sección "Siguiente paso")
            log.info(
                "🔔 Recordatorio a %s: %s @ %s UTC",
                usuario.email if usuario else "?",
                act.titulo,
                act.inicio.isoformat(),
            )
            r.enviado = True
            r.enviado_en = now_utc
        db.commit()
    except Exception:
        log.exception("error en recordatorios")
    finally:
        db.close()


def start_scheduler() -> BackgroundScheduler:
    sched = BackgroundScheduler(timezone="UTC")
    sched.add_job(process_reminders, "interval", seconds=30, id="reminders")
    sched.start()
    return sched