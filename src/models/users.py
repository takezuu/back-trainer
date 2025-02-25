import re
from datetime import datetime
from typing import Optional
from pydantic import EmailStr, field_validator
from sqlmodel import Field, SQLModel




class UserBase(SQLModel):
    username: str = Field(index=True)
    email: EmailStr = Field(index=True)
    phone: str = Field(index=True)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not (5 <= len(value) <= 15):
            raise ValueError("Длина логина должна быть от 5 до 15 символов.")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        phone_pattern = re.compile(r"^\+\d{11,15}$")
        if not phone_pattern.match(value):
            raise ValueError("Номер телефона должен соответствовать формату: + и от 11 до 15 цифр, например: +73423455443.")
        return value

class User(UserBase, table=True):
    __tablename__ = "users"  # Явно задаем имя таблицы, чтобы избежать конфликта

    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str
    ip_address: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    last_login_time: Optional[datetime] = Field(default=None, index=True)
    country_code: Optional[str] = Field(default=None, index=True)

    @field_validator("last_login_time", mode="before", check_fields=False)
    @classmethod
    def validate_last_login_time(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%I:%M %p")
            except ValueError:
                raise ValueError("Неверный формат времени. Ожидается 'HH:MM AM/PM'.")
        return value

class UserCreate(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not (5 <= len(value) <= 20):
            raise ValueError("Длина пароля должна быть от 5 до 20 символов.")
        return value

class UserID(SQLModel):
    id: int
 
    

class UserRead(SQLModel):
    id: int
    username: str = Field(index=True)
    email: str = Field(index=True)
    ip_address: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    last_login_time: Optional[datetime] = None
    country_code: str = Field(index=True)
    phone: str = Field(index=True)

    @field_validator("last_login_time", mode="before", check_fields=False)
    @classmethod
    def validate_last_login_time(cls, value):
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%I:%M %p")
            except ValueError:
                raise ValueError("Неверный формат времени. Ожидается 'HH:MM AM/PM'.")
        return value
  