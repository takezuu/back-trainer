import re
from datetime import date, datetime
from fastapi import HTTPException
from pydantic import field_validator, root_validator, model_validator
from sqlmodel import Field, SQLModel


class UsersModels:
    class Users(SQLModel, table=True):
        id: int = Field(primary_key=True, index=True)
        username: str = Field(index=True, nullable=False)
        email: str = Field(index=True)
        password_hash: str = Field(index=True)
        ip_address: str = Field(index=True)
        created_at: date = Field(index=True)
        last_login_time: str = Field(index=True)
        country_code: str = Field(index=True)
        phone: str = Field(index=True, nullable=False)

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
            return value

        @field_validator("email")
        def validate_email(cls, value: str):
            email_pattern = re.compile(r'[a-z\d_\.]{1,25}@[a-z\d_]{1,25}\.[a-z]{2,3}')
            result = email_pattern.match(value)
            if not result:
                raise HTTPException(status_code=404, detail="wrong email pattern")
            if len(value) < 5 or len(value) > 30:
                raise HTTPException(status_code=404, detail="email length should be from 5 to 30 characters")
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
            return value

        @field_validator("password")
        def validate_password(cls, value: str):
            if len(value) < 5 or len(value) > 20:
                raise HTTPException(status_code=404, detail="password length should be from 5 to 20 characters")
            return value
