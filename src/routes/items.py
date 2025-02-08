from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel import select
from src import schemas, models
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/items", tags=["items"], response_model=List[schemas.Items])
async def read_users(session: SessionDep):
    customer = session.exec(select(models.Items)).all()
    return customer


@router.get("/items/{item_id}", tags=["items"], response_model=schemas.Items)
async def read_users(item_id: int, session: SessionDep):
    statement = select(models.Items).where(models.Items.id == item_id)
    item = session.exec(statement).first()
    return item
