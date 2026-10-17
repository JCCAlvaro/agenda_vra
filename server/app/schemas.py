from datetime import datetime, timezone
from typing import Annotated

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    PlainSerializer,
    field_validator,
)


def _serialize_dt(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()


UTCDateTime = Annotated[datetime, PlainSerializer(_serialize_dt, return_type=str)]


class LoginReq(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: str
    email: str
    nombre: str
    rol: str
    model_config = {"from_attributes": True}


class LoginResp(BaseModel):
    token: str
    user: UserOut


class ActividadIn(BaseModel):
    titulo: str = Field(min_length=1, max_length=255)
    descripcion: str | None = None
    inicio: datetime
    fin: datetime
    lugar: str | None = None
    prioridad: str = "media"
    origen: str = "interna"
    recordatorio_min: int = 0

    @field_validator("inicio", "fin", mode="before")
    @classmethod
    def _to_utc_naive(cls, v):
        if isinstance(v, str):
            v = datetime.fromisoformat(v.replace("Z", "+00:00"))
        if isinstance(v, datetime) and v.tzinfo is not None:
            v = v.astimezone(timezone.utc).replace(tzinfo=None)
        return v


class ActividadOut(BaseModel):
    id: str
    titulo: str
    descripcion: str | None = None
    inicio: UTCDateTime
    fin: UTCDateTime
    lugar: str | None = None
    prioridad: str
    estado: str
    origen: str
    creado_por: str
    creado_en: UTCDateTime
    model_config = {"from_attributes": True}