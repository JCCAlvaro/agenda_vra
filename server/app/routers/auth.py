from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Usuario
from ..schemas import LoginReq, LoginResp, UserOut
from ..security import verify_password, create_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResp)
def login(body: LoginReq, db: Session = Depends(get_db)):
    user = db.query(Usuario).filter(Usuario.email == body.email).first()
    if not user or not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "credenciales inválidas")
    token = create_token(user.id, user.email, user.rol)
    return {"token": token, "user": UserOut.model_validate(user)}