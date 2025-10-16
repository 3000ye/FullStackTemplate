from backend.db import get_base_client_db
from backend.db.crud.system_user import add_user
from backend.db.model.system import UserCreate


if __name__ == '__main__':
    with get_base_client_db() as db:
        add_user(
            UserCreate(
                name="admin",
                role="admin",
                status=1,
                password="fullstacktemplate"
            ), db
        )