from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import case
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import current_user
from ..models import Actividad, Recordatorio, Auditoria, Usuario
from ..schemas import ActividadIn, ActividadOut

router = APIRouter(prefix="/actividades", tags=["actividades"])


@router.get("", response_model=list[ActividadOut])
def listar(
    desde: datetime | None = Query(None),
    hasta: datetime | None = Query(None),
    db: Session = Depends(get_db),
    user: Usuario = Depends(current_user),
):
    q = db.query(Actividad)
    if desde:
        q = q.filter(Actividad.fin >= desde)
    if hasta:
        q = q.filter(Actividad.inicio <= hasta)
    orden = case(
        (Actividad.prioridad == "alta", 1),
        (Actividad.prioridad == "media", 2),
        else_=3,
    )
    return q.order_by(orden, Actividad.inicio).all()


@router.get("/{aid}", response_model=ActividadOut)
def obtener(
    aid: str,
    db: Session = Depends(get_db),
    user: Usuario = Depends(current_user),
):
    a = db.query(Actividad).filter(Actividad.id == aid).first()
    if not a:
        raise HTTPException(404, "no encontrada")
    return a


@router.post("", status_code=201)
def crear(
    body: ActividadIn,
    db: Session = Depends(get_db),
    user: Usuario = Depends(current_user),
):
    a = Actividad(
        titulo=body.titulo,
        descripcion=body.descripcion,
        inicio=body.inicio,
        fin=body.fin,
        lugar=body.lugar,
        prioridad=body.prioridad,
        origen=body.origen,
        creado_por=user.id,
    )
    db.add(a)
    db.flush()
    if body.recordatorio_min > 0:
        db.add(
            Recordatorio(
                actividad_id=a.id,
                enviar_en=body.inicio - timedelta(minutes=body.recordatorio_min),
            )
        )
    db.add(
        Auditoria(usuario_id=user.id, accion="create", entidad="actividad", entidad_id=a.id)
    )
    db.commit()
    return {"id": a.id}


@router.put("/{aid}")
def actualizar(
    aid: str,
    body: ActividadIn,
    db: Session = Depends(get_db),
    user: Usuario = Depends(current_user),
):
    a = db.query(Actividad).filter(Actividad.id == aid).first()
    if not a:
        raise HTTPException(404, "no encontrada")
    a.titulo = body.titulo
    a.descripcion = body.descripcion
    a.inicio = body.inicio
    a.fin = body.fin
    a.lugar = body.lugar
    a.prioridad = body.prioridad
    a.origen = body.origen
    db.add(
        Auditoria(usuario_id=user.id, accion="update", entidad="actividad", entidad_id=a.id)
    )
    db.commit()
    return {"ok": True}


@router.delete("/{aid}")
def eliminar(
    aid: str,
    db: Session = Depends(get_db),
    user: Usuario = Depends(current_user),
):
    a = db.query(Actividad).filter(Actividad.id == aid).first()
    if not a:
        raise HTTPException(404, "no encontrada")
    db.delete(a)
    db.add(
        Auditoria(usuario_id=user.id, accion="delete", entidad="actividad", entidad_id=aid)
    )
    db.commit()
    return {"ok": True}