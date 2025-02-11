from datetime import date
from sqlmodel import Field, SQLModel

class CustomersModel(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    user_id: int = Field(index=True)
    first_name: str = Field(index=True)
    last_name: str = Field(index=True)
    address: str | None = Field(default=None, index=True)
    contact_phone: str | None = Field(default=None, index=True)
    date_of_birth: date | None = Field(default=None, index=True)
