from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError
from typing import Annotated, Type
from typing_extensions import TypeAlias
from sqlmodel import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from backend.db import get_base_db
from backend.core.system_auth import decode_access_token
from backend.db.model.system import User, TokenPayload


SessionDep: TypeAlias = Annotated[Session, Depends(get_base_db)]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/system/auth/token")
TokenDep = Annotated[str, Depends(oauth2_scheme)]


def get_current_user(db: SessionDep, token: TokenDep) -> Type[User]:
    try:
        payload = decode_access_token(token)
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    user = db.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.status != 1:
        raise HTTPException(status_code=400, detail="User disabled")

    return user

CurrentUser: TypeAlias = Annotated[User, Depends(get_current_user)]

def check_current_user_admin(current_user: CurrentUser) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")

    return current_user
