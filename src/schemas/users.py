from datetime import date
from pydantic import BaseModel


class Users(BaseModel):
    id: int
    username: str
    email: str
    ip_address: str
    created_at: date
    last_login_time: str
    country_code: str
    phone: str