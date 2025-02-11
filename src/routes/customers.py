from datetime import date
from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel import select
from src import schemas, models
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/api/customers", tags=["customers"], response_model=List[schemas.Customers])
async def get_customers(session: SessionDep,
                     first_name: str = None,
                     last_name: str = None,
                     contact_phone: str = None,
                     date_of_birth: date = None,
                     q: str = None,
                     sort: str = "id",
                     order_by: str = "asc",
                     page: int = 1,
                     limit: int = 25
                     ):
    customers = models.Customers
    query = select(customers)

    if first_name:
        query = query.where(customers.first_name == first_name)
    if last_name:
        query = query.where(customers.last_name == last_name)
    if contact_phone:
        query = query.where(customers.contact_phone == contact_phone)
    if date_of_birth:
        query = query.where(customers.date_of_birth == date_of_birth)
    if q:
        query = query.where((customers.first_name.contains(q)) | (customers.last_name.contains(q)))

    order = getattr(customers, sort)
    if order_by == "desc":
        order = order.desc()
    query = query.order_by(order)

    query = query.offset((page - 1) * limit).limit(limit)
    return session.exec(query).all()


@router.get("/api/customers/{customer_id}", tags=["customers"], response_model=schemas.Customers)
async def get_customer(customer_id: int, session: SessionDep):
    statement = select(models.Customers).where(models.Customers.id == customer_id)
    customer = session.exec(statement).first()
    return customer
