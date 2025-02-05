from datetime import date

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str
    ip_address: str
    created_at: date
    last_login_time: str
    country_code: str
    phone: str


class Customer(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    address: str | None
    contact_phone: str | None
    date_of_birth: date | None
