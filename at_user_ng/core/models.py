from pydantic import BaseModel


class UserData(BaseModel):
    id: int

    last_login: str
    is_superuser: bool
    username: str
    first_name: str
    last_name: str
    email: str
    is_staff: bool
    is_active: bool
    date_joined: str
    groups: list
    user_permissions: list
