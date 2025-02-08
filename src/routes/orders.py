from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel import select
from src import schemas, models
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/orders", tags=["orders"], response_model=List[schemas.Orders])
async def read_users(session: SessionDep):
    customer = session.exec(select(models.Orders)).all()
    return customer


@router.get("/orders/{order_id}", tags=["orders"], response_model=schemas.Orders)
async def read_users(order_id: int, session: SessionDep):
    statement = select(models.Orders).where(models.Orders.id == order_id)
    order = session.exec(statement).first()
    return order
