import re
from datetime import datetime
from fastapi import HTTPException
from pydantic import field_validator
from sqlmodel import Field, SQLModel


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
    email: str = Field(index=True)
    phone: str = Field(index=True)
    full_name: str = Field(index=True)
    password: str = Field(index=True)
    can_delete: bool = Field(index=True, default=True)

    @field_validator("full_name")
    def validate_full_name(cls, value: str):
        if len(value) < 5 or len(value) > 15:
            raise HTTPException(status_code=400, detail="Full name length should be from 5 to 100 characters")
        full_name_pattern = re.compile(r'^[A-z]{1,30} [A-z]{1,30}$')
        result = full_name_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400, detail="Available only latin letters and space between words")
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Full name should be Str type")
        return value

    @field_validator("email")
    def validate_email(cls, value: str):
        email_pattern = re.compile(r'[A-z\d_\.]{1,25}@[A-z\d_]{1,25}\.[A-z]{2,3}')
        result = email_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400, detail="Wrong email pattern")
        if len(value) < 5 or len(value) > 30:
            raise HTTPException(status_code=400, detail="Email length should be from 5 to 30 characters")
        if ' ' in value:
            raise HTTPException(status_code=400, detail="Space in email")
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Email should be Str type")
        return value

    @field_validator("phone")
    def validate_phone(cls, value: str):
        phone_pattern = re.compile(r"\+\d{11,15}")
        result = phone_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400,
                                detail="Phone pattern is: + and digits from 11 to 15 example: +73423455443")
        if len(value) < 12 or len(value) > 16:
            raise HTTPException(status_code=400, detail="Phone length should be from 12 to 16 characters")
        if not value[1:].isdigit():
            raise HTTPException(status_code=400, detail="Available only latin letters and digits")
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Phone should be Str type")
        return value

    @field_validator("password")
    def validate_password(cls, value: str):
        if len(value) < 5 or len(value) > 20:
            raise HTTPException(status_code=400, detail="Password length should be from 5 to 20 characters")
        if not value.isalnum():
            raise HTTPException(status_code=400, detail="Available only latin letters and digits in password")
        if not any(char.isdigit() for char in value):
            raise HTTPException(status_code=400, detail="Password should have at least one numeral")
        if not any(char.isupper() for char in value):
            raise HTTPException(status_code=400, detail="Password should have at least one uppercase letter")
        if not any(char.islower() for char in value):
            raise HTTPException(status_code=400, detail="Password should have at least one lowercase letter")
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Password should be Str type")
        return value


class UsersResponse(SQLModel):
    id: int
    email: str
    phone: str
    full_name: str
    ip_address: str | None
    last_login_time: datetime | None
    country_code: str | None


class UserPut(SQLModel):
    email: str
    phone: str
    full_name: str
    balance: int

    @field_validator("full_name")
    def validate_full_name(cls, value: str):
        if len(value) < 5 or len(value) > 15:
            raise HTTPException(status_code=400, detail="Full name length should be from 5 to 100 characters")
        full_name_pattern = re.compile(r'^[A-z]{1,30} [A-z]{1,30}$')
        result = full_name_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400, detail="Available only latin letters and space between words")
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Full name should be Str type")
        return value

    @field_validator("email")
    def validate_email(cls, value: str):
        email_pattern = re.compile(r'[A-z\d_\.]{1,25}@[A-z\d_]{1,25}\.[A-z]{2,3}')
        result = email_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400, detail="Wrong email pattern")
        if len(value) < 5 or len(value) > 30:
            raise HTTPException(status_code=400, detail="Email length should be from 5 to 30 characters")
        if ' ' in value:
            raise HTTPException(status_code=400, detail="Space in email")
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Email should be Str type")
        return value

    @field_validator("phone")
    def validate_phone(cls, value: str):
        phone_pattern = re.compile(r"\+\d{11,15}")
        result = phone_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400,
                                detail="Phone pattern is: + and digits from 11 to 15 example: +73423455443")
        if len(value) < 12 or len(value) > 16:
            raise HTTPException(status_code=400, detail="Phone length should be from 12 to 16 characters")
        if not value[1:].isdigit():
            raise HTTPException(status_code=400, detail="Available only latin letters and digits")
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Phone should be Str type")
        return value


class UserUpdatedResponse(SQLModel):
    message: str
    updated_user: UsersResponse


class UserAddedResponse(SQLModel):
    id: int


class UserPatch(SQLModel):
    email: str | None = None
    phone: str | None = None
    full_name: str | None = None

class UserPatchResponse(SQLModel):
    id: int
    email: str
    phone: str
    full_name: str
    ip_address: str
    last_login_time: datetime
    balance: int
    can_delete: bool
