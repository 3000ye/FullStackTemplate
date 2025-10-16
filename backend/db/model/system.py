from typing import Optional
from sqlmodel import Field, SQLModel, Column
from sqlalchemy import text
from datetime import datetime
from enum import Enum


# region system token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: Optional[str] = None
# endregion

# region system user
class UserRole(str, Enum):
    admin = "admin"
    normal = "normal"
    manager = "manager"


class UserBase(SQLModel):
    name: str = Field(default=None, max_length=50, nullable=False, title="用户名")
    role: str = Field(default=None, nullable=False, title="用户角色")
    status: int = Field(default=None, title="状态：启用=1，禁用=0")


class UserCreate(UserBase):
    password: str = Field(min_length=6, max_length=40, title="密码")


class UserUpdate(UserBase):
    id: Optional[int] = Field(default=None, title="用户 ID")
    password: Optional[str] = Field(default=None, min_length=6, max_length=40, title="密码")


class UserResponse(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime


class UserQuery(SQLModel):
    name: Optional[str] = Field(None, max_length=50, title="用户名")
    role: Optional[UserRole] = Field(None, title="用户角色")
    status: Optional[int] = Field(None, title="状态")
    skip: Optional[int] = Field(None)
    limit: Optional[int] = Field(None)


class User(UserBase, table=True):
    """数据库 Model"""
    __tablename__ = "system_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    pwd_hash: str = Field(nullable=False, max_length=255, title="密码哈希")
    created_at: datetime = Field(sa_column=Column(nullable=False, server_default=text("CURRENT_TIMESTAMP")))
    updated_at: datetime = Field(sa_column=Column(nullable=False, server_default=text("CURRENT_TIMESTAMP"), server_onupdate=text("CURRENT_TIMESTAMP")))
# endregion
