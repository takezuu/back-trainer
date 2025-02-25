import re
from datetime import date, datetime
from fastapi import HTTPException
from pydantic import field_validator, root_validator, model_validator
from sqlmodel import Field, SQLModel
import hashlib


class UsersModels:
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

    class UserAddedResponse(SQLModel):
        id: int

    class UserAdd(SQLModel):
        username: str
        email: str
        phone: str
        password: str
        created_at: str = Field(default_factory=lambda: datetime.today().strftime("%m/%d/%Y"))

        @field_validator("username")
        def validate_username(cls, value: str):
            if len(value) < 5 or len(value) > 15:
                raise HTTPException(status_code=404, detail="login length should be from 5 to 15 characters")
            if not value.isalnum():
                raise HTTPException(status_code=404, detail="available only latin letters and digits in username")
            return value

        @field_validator("email")
        def validate_email(cls, value: str):
            email_pattern = re.compile(r'[A-z\d_\.]{1,25}@[A-z\d_]{1,25}\.[A-z]{2,3}')
            result = email_pattern.match(value)
            if not result:
                raise HTTPException(status_code=404, detail="wrong email pattern")
            if len(value) < 5 or len(value) > 30:
                raise HTTPException(status_code=404, detail="email length should be from 5 to 30 characters")
            if ' ' in value:
                raise HTTPException(status_code=404, detail="space in email")
            return value

        @field_validator("phone")
        def validate_phone(cls, value: str):
            phone_pattern = re.compile(r"\+\d{11,15}")
            result = phone_pattern.match(value)
            if not result:
                raise HTTPException(status_code=404,
                                    detail="phone pattern is: + and digits from 11 to 15 example: +73423455443")
            if len(value) < 12 or len(value) > 16:
                raise HTTPException(status_code=404, detail="phone length should be from 12 to 16 characters")
            if not value[1:].isdigit():
                raise HTTPException(status_code=404, detail="available only latin letters and digits")
            return value

        @field_validator("password")
        def validate_password(cls, value: str):
            if len(value) < 5 or len(value) > 20:
                raise HTTPException(status_code=404, detail="password length should be from 5 to 20 characters")
            if not value.isalnum():
                raise HTTPException(status_code=404, detail="available only latin letters and digits in password")
            if not any(char.isdigit() for char in value):
                raise HTTPException(status_code=404, detail="password should have at least one numeral")
            if not any(char.isupper() for char in value):
                raise HTTPException(status_code=404, detail="password should have at least one uppercase letter")
            if not any(char.islower() for char in value):
                raise HTTPException(status_code=404, detail="Password should have at least one lowercase letter")

            salt = "5gz"
            value = value + salt
            value = hashlib.md5(value.encode())
            return value
