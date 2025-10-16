from fastapi import HTTPException
from sqlmodel import Session, select, func
import traceback

from backend.db.model.system import User, UserCreate, UserUpdate, UserQuery
from backend.core.system_auth import hash_password
from backend.utils.logger import Logger

logger = Logger(name=__name__)


def add_user(item: UserCreate, db: Session):
    """
    新增用户，admin 使用，非注册入口
    """

    db_user = db.scalars(select(User).where(User.name == item.name)).one_or_none()
    if db_user:
        raise HTTPException(status_code=500, detail="user already exists")

    _add = item.model_dump()
    _add["pwd_hash"] = hash_password(_add.pop("password"))
    _add_user = User(**_add)

    try:
        db.add(_add_user)
        db.commit()
        db.refresh(_add_user)
        return { "code": "0", "msg": "success", "user": _add_user }
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(error_detail)
        raise HTTPException(status_code=500, detail=error_detail)

def update_user(item: UserUpdate, db: Session):
    """
    修改用户信息，admin 使用
    """

    if not item.id:
        raise HTTPException(status_code=404, detail="user id not found")

    db_user = db.get(User, item.id)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")

    item_data = item.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in item_data:
        extra_data["pwd_hash"] = hash_password(item_data["password"])

    try:
        db_user.sqlmodel_update(item_data, update=extra_data)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return { "code": "0", "msg": "success", "user": db_user }
    except Exception as e:
        error_detail = traceback.format_exc()
        logger.error(error_detail)
        raise HTTPException(status_code=500, detail=error_detail)

def query_user(item: UserQuery, db: Session):
    """
    查询已有用户，可选：名称，角色，状态，admin 使用
    """

    stmt = select(User)

    if item.name:
        stmt = stmt.where(User.name.like(f"%{item.name}%"))
    if item.role:
        stmt = stmt.where(User.role == item.role)
    if item.status:
        stmt = stmt.where(User.status == item.status)

    count = db.scalar(select(func.count()).select_from(stmt.subquery()))

    if item.skip:
        stmt = stmt.offset(item.skip)
    if item.limit:
        stmt = stmt.limit(item.limit)

    user_list = db.scalars(stmt).all()

    return { "code": "0", "msg": "success", "user_list": user_list, "count": count }

def query_by_username(name: str, db: Session):
    """
    通过用户名查询用户，用于登陆使用
    """

    db_user = db.scalars(select(User).where(User.name == name)).one_or_none()

    if db_user:
        return { "code": "0", "msg": "success", "user": db_user }
    else:
        raise HTTPException(status_code=404, detail="user not found")