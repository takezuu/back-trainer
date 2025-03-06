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
    country_code: str = Field(index=True)
    can_delete: bool = Field(index=True)


class UserAdd(SQLModel):
    full_name: str = Field(index=True)
    email: str = Field(index=True)
    phone: str = Field(index=True)
    password: str = Field(index=True)
    can_delete: bool | None = Field(index=True, default=True)

    @field_validator("full_name")
    def validate_full_name(cls, value: str):
        full_name_pattern = re.compile(r'[A-Za-z]{1,30} [A-Za-z]{1,30}$')
        result = full_name_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400,
                                detail="Full name must be two words with Latin letters, 5-15 characters total")
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Full name should be Str type")
        return value

    @field_validator("email")
    def validate_email(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Email should be Str type")
        email_pattern = re.compile(r'^[A-Za-z\d._]{1,25}@[A-Za-z\d_]{1,25}\.[A-Za-z]{2,3}$')
        result = email_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400, detail="Invalid email format (e.g., user@domain.com)")
        return value

    @field_validator("password")
    def validate_password(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400,
                                detail="Password should be Str type")
        password_pattern = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z\d]{5,20}$")
        result = password_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400,
                                detail="Password must be 5-20 characters long and contain at least one number, one uppercase and one lowercase letter")
        return value

    @field_validator("phone")
    def validate_phone(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Phone should be Str type")
        phone_pattern = re.compile(r"^\+\d{11,15}$")
        result = phone_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400,
                                detail="Phone must start with + followed by 11-15 digits (e.g., +73423455443)")
        return value

    @field_validator("can_delete")
    def validate_can_delete(cls, value: bool):
        if not isinstance(value, bool):
            raise HTTPException(status_code=400, detail="Can_delete should be Bool type")
        value = True
        return value

class UsersResponse(SQLModel):
    id: int
    email: str
    phone: str
    full_name: str
    ip_address: str | None
    country_code: str | None
    can_delete: bool

class UserResponse(UsersResponse):
    completed_orders: list[int] | None
    uncompleted_orders: list[int] | None


class UserPut(SQLModel):
    full_name: str
    email: str
    phone: str
    country_code: str

    @field_validator("full_name")
    def validate_full_name(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Full name should be Str type")
        full_name_pattern = re.compile(r'[A-Za-z]{1,30} [A-Za-z]{1,30}$')
        result = full_name_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400,
                                detail="Full name must be two words with Latin letters, 5-15 characters total")
        return value

    @field_validator("email")
    def validate_email(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Email should be Str type")
        email_pattern = re.compile(r'^[A-Za-z\d._]{1,25}@[A-Za-z\d_]{1,25}\.[A-Za-z]{2,3}$')
        result = email_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400, detail="Invalid email format (e.g., user@domain.com)")

        return value

    @field_validator("phone")
    def validate_phone(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Phone should be Str type")
        phone_pattern = re.compile(r"^\+\d{11,15}$")
        result = phone_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400,
                                detail="Phone must start with + followed by 11-15 digits (e.g., +73423455443)")
        return value

    @field_validator("country_code")
    def validate_country_code(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="County code should be Str type")
        if len(value) > 3:
            raise HTTPException(status_code=400, detail="County code length should be less than 3")
        if not value.isalpha():
            raise HTTPException(status_code=400, detail="County code should have only latin letters")
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
    country_code: str | None = None

    @field_validator("full_name")
    def validate_full_name(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Full name should be Str type")
        full_name_pattern = re.compile(r'[A-Za-z]{1,30} [A-Za-z]{1,30}$')
        result = full_name_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400, detail="Full name must be two words with Latin letters, 5-15 characters total")
        return value

    @field_validator("email")
    def validate_email(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Email should be Str type")
        email_pattern = re.compile(r'^[A-Za-z\d._]{1,25}@[A-Za-z\d_]{1,25}\.[A-Za-z]{2,3}$')
        result = email_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400, detail="Invalid email format (e.g., user@domain.com)")
        return value

    @field_validator("phone")
    def validate_phone(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="Phone should be Str type")
        phone_pattern = re.compile(r"^\+\d{11,15}$")
        result = phone_pattern.match(value)
        if not result:
            raise HTTPException(status_code=400,
                                detail="Phone must start with + followed by 11-15 digits (e.g., +73423455443)")
        return value

    @field_validator("country_code")
    def validate_country_code(cls, value: str):
        if not isinstance(value, str):
            raise HTTPException(status_code=400, detail="County code should be Str type")
        if len(value) > 3:
            raise HTTPException(status_code=400, detail="County code length should be less than 3")
        if not value.isalpha():
            raise HTTPException(status_code=400, detail="County code should have only latin letters")
        return value
