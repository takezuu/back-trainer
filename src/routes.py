from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel import select
from src import schemas, models
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/users", tags=["users"], response_model=List[schemas.Users])
async def read_users(session: SessionDep):
    users = session.exec(select(models.Users)).all()
    return users


@router.get("/customers", tags=["customers"], response_model=List[schemas.Customers])
async def read_users(session: SessionDep):
    customer = session.exec(select(models.Customers)).all()
    return customer


@router.get("/orders", tags=["orders"], response_model=List[schemas.Orders])
async def read_users(session: SessionDep):
    customer = session.exec(select(models.Orders)).all()
    return customer


@router.get("/items", tags=["items"], response_model=List[schemas.Items])
async def read_users(session: SessionDep):
    customer = session.exec(select(models.Items)).all()
    return customer
