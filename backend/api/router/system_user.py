from fastapi import HTTPException, APIRouter, Depends

from backend.api.deps import SessionDep, check_current_user_admin, CurrentUser
from backend.db.crud.system_user import add_user, update_user, query_user
from backend.db.model.system import UserCreate, UserUpdate, UserResponse, UserQuery

router = APIRouter()


@router.post("/create_user", dependencies=[Depends(check_current_user_admin)], response_model=UserResponse)
def system_create_user(user: UserCreate, db: SessionDep):
    """
    新增用户，admin 使用，非注册入口
    """

    res = add_user(user, db)
    if res["code"] == "0":
        return res["user"]
    else:
        raise HTTPException(status_code=500, detail=res["msg"])

@router.post("/delete_user", dependencies=[Depends(check_current_user_admin)], response_model=UserResponse)
def system_delete_user(user: UserUpdate, db: SessionDep):
    """
    删除/禁用用户，逻辑删除，admin 使用
    """

    db_user = UserUpdate(id=user.id, status=0)
    res = update_user(db_user, db)
    if res["code"] == "0":
        return res["user"]
    else:
        raise HTTPException(status_code=500, detail=res["msg"])

@router.post("/update_user", dependencies=[Depends(check_current_user_admin)], response_model=UserResponse)
def system_update_user(user: UserUpdate, db: SessionDep):
    """
    修改用户信息，admin 使用
    """

    res = update_user(user, db)
    if res["code"] == "0":
        return res["user"]
    else:
        raise HTTPException(status_code=500, detail=res["msg"])

@router.post("/query_user", dependencies=[Depends(check_current_user_admin)])
def system_query_user(user: UserQuery, db: SessionDep):
    """
    查询已有用户，可选：名称，角色，状态，admin 使用
    """

    res = query_user(user, db)
    if res["code"] == "0":
        return { "data": res["user_list"], "count": res["count"] }
    else:
        raise HTTPException(status_code=500, detail=res["msg"])

@router.post("/query_self")
def system_query_self(current_user: CurrentUser):
    return current_user

@router.post("/update_self")
def system_update_self(user: UserUpdate, db: SessionDep):
    res = update_user(user, db)
    if res["code"] == "0":
        return res["user"]
    else:
        raise HTTPException(status_code=500, detail=res["msg"])
