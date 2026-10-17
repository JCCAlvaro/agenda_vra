from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import require_role
from ..models import Usuario
from ..schemas import UserOut

router = APIRouter(prefix="/usuarios", tags=["usuarios"])


@router.get("", response_model=list[UserOut])
def listar(
    db: Session = Depends(get_db),
    user=Depends(require_role("admin", "vicerrector")),
):
    return db.query(Usuario).order_by(Usuario.nombre).all()