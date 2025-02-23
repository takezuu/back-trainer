from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException

from sqlmodel import Session
from sqlmodel import select

from src.schemas.users import UsersSchemas
from src.models.users import UsersModels
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/api/users", tags=["users"], response_model=List[UsersSchemas.Users])
async def get_users(session: SessionDep,
                    username: str = None,
                    email: str = None,
                    country_code: str = None,
                    q: str = None,
                    sort: str = "id",
                    order_by: str = "asc",
                    page: int = 1, limit: int = 25):
    users = UsersModels.Users
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


@router.get("/api/users/{user_id}", tags=["users"], response_model=UsersSchemas.Users)
async def get_user(user_id: int, session: SessionDep):
    query = select(UsersModels.Users).where(UsersModels.Users.id == user_id)
    user = session.exec(query).first()
    return user


@router.post("/api/users", tags=["users"], response_model=UsersSchemas.UserAdded)
async def create_user(user: UsersModels.UserAdd, session: SessionDep):
    print(user)
    db_user = UsersModels.Users(**user.model_dump())

    if db_user.phone:
        query = select(UsersModels.Users).where(UsersModels.Users.phone == db_user.phone)
        phone_exists = session.exec(query).first() is not None
        if phone_exists:
            raise HTTPException(status_code=404, detail="Phone is already use")

    if db_user.email:
        query = select(UsersModels.Users).where(UsersModels.Users.email == db_user.email)
        email_exists = session.exec(query).first() is not None
        if email_exists:
            raise HTTPException(status_code=404, detail="Email is already use")

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
