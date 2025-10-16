from fastapi import APIRouter

from backend.api.router import system_auth
from backend.api.router import system_user
from backend.utils.logger import Logger

logger = Logger(name=__name__)


api_router = APIRouter()
api_router.include_router(system_auth.router, prefix="/system/auth", tags=["system auth"])

# 以下 router 的 prefix 使用 new_router 创建
api_router.include_router(system_user.router, prefix="/user", tags=["system user"])
