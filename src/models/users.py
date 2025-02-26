import re
from datetime import date, datetime
from fastapi import HTTPException
from pydantic import field_validator
from sqlmodel import Field, SQLModel

class UsersModels:
    class Users(SQLModel, table=True):
        id: int = Field(primary_key=True, index=True)
        email: str = Field(index=True)
        phone: str = Field(index=True)
        full_name: str = Field(index=True)
        password: str = Field(index=True)
        ip_address: str = Field(index=True)
        last_login_time: datetime = Field(index=True)
        country_code: str = Field(index=True)
        balance: int = Field(index=True)
        can_delete: bool = Field(index=True)

    class UserAdd(SQLModel):
        email: str
        phone: str
        full_name: str
        password: str
        can_delete: bool = True

        @field_validator("full_name")
        def validate_username(cls, value: str):
            if len(value) < 5 or len(value) > 15:
                raise HTTPException(status_code=400, detail="login length should be from 5 to 100 characters")
            full_name_pattern = re.compile(r'^[A-z]{1,30} [A-z]{1,30}$')
            result = full_name_pattern.match(value)
            if not result:
                raise HTTPException(status_code=400, detail="available only latin letters and space between words")
            return value

        @field_validator("email")
        def validate_email(cls, value: str):
            email_pattern = re.compile(r'[A-z\d_\.]{1,25}@[A-z\d_]{1,25}\.[A-z]{2,3}')
            result = email_pattern.match(value)
            if not result:
                raise HTTPException(status_code=400, detail="wrong email pattern")
            if len(value) < 5 or len(value) > 30:
                raise HTTPException(status_code=400, detail="email length should be from 5 to 30 characters")
            if ' ' in value:
                raise HTTPException(status_code=400, detail="space in email")
            return value

        @field_validator("phone")
        def validate_phone(cls, value: str):
            phone_pattern = re.compile(r"\+\d{11,15}")
            result = phone_pattern.match(value)
            if not result:
                raise HTTPException(status_code=400,
                                    detail="phone pattern is: + and digits from 11 to 15 example: +73423455443")
            if len(value) < 12 or len(value) > 16:
                raise HTTPException(status_code=400, detail="phone length should be from 12 to 16 characters")
            if not value[1:].isdigit():
                raise HTTPException(status_code=400, detail="available only latin letters and digits")
            return value

        @field_validator("password")
        def validate_password(cls, value: str):
            if len(value) < 5 or len(value) > 20:
                raise HTTPException(status_code=400, detail="password length should be from 5 to 20 characters")
            if not value.isalnum():
                raise HTTPException(status_code=400, detail="available only latin letters and digits in password")
            if not any(char.isdigit() for char in value):
                raise HTTPException(status_code=400, detail="password should have at least one numeral")
            if not any(char.isupper() for char in value):
                raise HTTPException(status_code=400, detail="password should have at least one uppercase letter")
            if not any(char.islower() for char in value):
                raise HTTPException(status_code=400, detail="Password should have at least one lowercase letter")
            return value

    class UsersResponse(SQLModel, table=True):
        id: int = Field(primary_key=True, index=True)
        email: str = Field(index=True)
        phone: str = Field(index=True)
        full_name: str = Field(index=True)
        ip_address: str = Field(index=True)
        last_login_time: datetime = Field(index=True)
        country_code: str = Field(index=True)

    class UserAddedResponse(SQLModel):
        id: int