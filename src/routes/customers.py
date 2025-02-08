from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel import select
from src import schemas, models
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/customers", tags=["customers"], response_model=List[schemas.Customers])
async def read_users(session: SessionDep):
    customer = session.exec(select(models.Customers)).all()
    return customer


@router.get("/customers/{customer_id}", tags=["customers"], response_model=schemas.Customers)
async def read_users(customer_id: int, session: SessionDep):
    statement = select(models.Customers).where(models.Customers.id == customer_id)
    customer = session.exec(statement).first()
    return customer
