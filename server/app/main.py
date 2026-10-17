import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import Base, engine, SessionLocal
from .deps import current_user
from .models import Usuario
from .scheduler import start_scheduler
from .schemas import UserOut
from .security import hash_password
from .routers import auth, actividades, dashboard, usuarios

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("app")


def seed_admin():
    db = SessionLocal()
    try:
        exists = db.query(Usuario).filter(Usuario.email == settings.ADMIN_EMAIL).first()
        if not exists:
            db.add(
                Usuario(
                    email=settings.ADMIN_EMAIL,
                    nombre="Administrador",
                    rol="admin",
                    password_hash=hash_password(settings.ADMIN_PASSWORD),
                )
            )
            db.commit()
            log.info("Admin creado: %s", settings.ADMIN_EMAIL)
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_admin()
    sched = start_scheduler()
    yield
    sched.shutdown()


app = FastAPI(title="Agenda Vicerrectorado UNAP", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(actividades.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")
app.include_router(usuarios.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"ok": True}


@app.get("/api/me", response_model=UserOut)
def me(user: Usuario = Depends(current_user)):
    return user