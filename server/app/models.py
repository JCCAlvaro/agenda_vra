import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


def uuid4_str() -> str:
    return str(uuid.uuid4())


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[str] = mapped_column(String(50), default="asistente")
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Actividad(Base):
    __tablename__ = "actividades"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    titulo: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    inicio: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)
    fin: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    lugar: Mapped[str | None] = mapped_column(String(255), nullable=True)
    prioridad: Mapped[str] = mapped_column(String(20), default="media")
    estado: Mapped[str] = mapped_column(String(20), default="pendiente")
    origen: Mapped[str] = mapped_column(String(20), default="interna")
    creado_por: Mapped[str] = mapped_column(String(36), ForeignKey("usuarios.id"))
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class Recordatorio(Base):
    __tablename__ = "recordatorios"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    actividad_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("actividades.id", ondelete="CASCADE")
    )
    enviar_en: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    enviado: Mapped[bool] = mapped_column(Boolean, default=False)
    enviado_en: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class Auditoria(Base):
    __tablename__ = "auditoria"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid4_str)
    usuario_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("usuarios.id"), nullable=True
    )
    accion: Mapped[str] = mapped_column(String(50), nullable=False)
    entidad: Mapped[str] = mapped_column(String(50), nullable=False)
    entidad_id: Mapped[str | None] = mapped_column(String(36), nullable=True)
    detalle: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)