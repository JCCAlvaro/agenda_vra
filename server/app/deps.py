from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import get_db
from .models import Usuario
from .security import decode_token

bearer = HTTPBearer(auto_error=False)


def current_user(
    cred: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
) -> Usuario:
    if cred is None:
        raise HTTPException(401, "no token")
    payload = decode_token(cred.credentials)
    if not payload:
        raise HTTPException(401, "token inválido")
    user = db.query(Usuario).filter(Usuario.id == payload["uid"]).first()
    if not user:
        raise HTTPException(401, "usuario no existe")
    return user


def require_role(*roles: str):
    def checker(user: Usuario = Depends(current_user)) -> Usuario:
        if user.rol not in roles:
            raise HTTPException(403, "forbidden")
        return user

    return checker