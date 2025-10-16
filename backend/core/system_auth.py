from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
import jwt

from backend.core import base_config


auth = base_config["auth"]

def hash_password(pwd: str) -> str:
    """
    使用 bcrypt 对密码进行加密
    """

    pwd_bytes = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    pwd_hash = bcrypt.hashpw(pwd_bytes, salt)
    return pwd_hash.decode('utf-8')

def verify_password(pwd: str, pwd_hash: str) -> bool:
    return bcrypt.checkpw(pwd.encode("utf-8"), pwd_hash.encode("utf-8"))

def create_access_token(subject: str, expires_delta: Optional[timedelta] = None):
    """
    创建通行证密钥，用于登陆校验
    """

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, auth["SECRET_KEY"], algorithm=auth["ALGORITHM"])
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, auth["SECRET_KEY"], algorithms=[auth["ALGORITHM"]])
