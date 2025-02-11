from datetime import date
from sqlmodel import Field, SQLModel


class Users(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    username: str = Field(index=True)
    email: str = Field(index=True)
    password_hash: str = Field(index=True)
    ip_address: str = Field(index=True)
    created_at: date = Field(index=True)
    last_login_time: str = Field(index=True)
    country_code: str = Field(index=True)
    phone: str = Field(index=True)