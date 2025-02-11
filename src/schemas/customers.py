from datetime import date
from pydantic import BaseModel


class Customers(BaseModel):
    id: int
    user_id: int
    first_name: str
    last_name: str
    address: str | None
    contact_phone: str | None
    date_of_birth: date | None