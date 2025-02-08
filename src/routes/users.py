from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel import select
from src import schemas, models
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/users", tags=["users"], response_model=List[schemas.Users])
async def read_users(session: SessionDep,
                     username: str = None,
                     email: str = None,
                     country_code: str = None,
                     q: str = None,
                     sort: str = "id",
                     order_by: str = "asc",
                     page: int = 1, limit: int = 25):
    users = models.Users
    query = select(users)

    if username:
        query = query.where(users.username == username)
    if email:
        query = query.where(users.email == email)
    if country_code:
        query = query.where(users.country_code == country_code)
    if q:
        query = query.where((users.username.contains(q)) | (users.email.contains(q)))

    order = getattr(users, sort)
    if order_by == "desc":
        order = order.desc()
    query = query.order_by(order)

    query = query.offset((page - 1) * limit).limit(limit)
    return session.exec(query).all()


@router.get("/users/{user_id}", tags=["users"], response_model=schemas.Users)
async def read_users(user_id: int, session: SessionDep):
    statement = select(models.Users).where(models.Users.id == user_id)
    user = session.exec(statement).first()
    return user
