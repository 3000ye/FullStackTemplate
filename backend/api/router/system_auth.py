from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated
import jwt

from backend.utils.logger import Logger
from backend.api.deps import SessionDep, CurrentUser
from backend.db.model.system import Token, User
from backend.db.crud.system_auth import authenticate
from backend.core.system_auth import create_access_token

router = APIRouter()
logger = Logger(name=__name__)


@router.post("/token")
def login(db: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    """
    使用 oauth2 进行登录表单验证，登录之后 24 小时之内有效
    """

    try:
        user: User = authenticate(form_data.username, form_data.password, db)

        expires = timedelta(hours=24)
        logger.info(f"{user.name} login successfully")

        return Token(access_token=create_access_token(str(user.id), expires_delta=expires))
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/check_token")
def check_token(current_user: CurrentUser):
    return current_user
