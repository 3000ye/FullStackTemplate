from fastapi import HTTPException
from sqlmodel import Session, select
from typing import Optional

from backend.db.model.system import User
from backend.db.crud.system_user import query_by_username
from backend.core.system_auth import verify_password
from backend.utils.logger import Logger

logger = Logger(name=__name__)


def authenticate(name: str, password: str, db: Session) -> Optional[User]:
    db_user = query_by_username(name, db)["user"]

    if not verify_password(password, db_user.pwd_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")
    if db_user.status != 1:
        raise HTTPException(status_code=401, detail="User disabled")

    return db_user