from urllib import parse
from contextlib import contextmanager
from sqlmodel import Session, create_engine
from collections.abc import Generator

from backend.core import base_config
from backend.utils.logger import Logger

logger = Logger(name=__name__)


# ========== Base MySQL ==========
base_mysql_config = base_config["mysql"]["base"]
base_mysql_url = base_mysql_config["MYSQL_URL"].replace(
    "password", parse.quote(base_mysql_config["PASSWORD"])
)

base_mysql_engine = create_engine(
    base_mysql_url,
    pool_pre_ping=True,      # 检查连接可用性
    pool_recycle=1800,       # 30分钟重置连接
    pool_size=10,            # 池大小（根据服务规模调整）
    max_overflow=5,          # 超出部分
)

def get_base_db() -> Generator[Session, None, None]:
    with Session(base_mysql_engine) as session:
        yield session

@contextmanager
def get_base_client_db() -> Generator[Session, None, None]:
    with Session(base_mysql_engine) as session:
        yield session
