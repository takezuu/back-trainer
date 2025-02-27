import hashlib
from typing import List, Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel import Session
from sqlmodel import select

from src.dependencies.users import user_exists
from src.models.users import UsersModels
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/api/users", tags=["users"], status_code=status.HTTP_200_OK,
            response_model=List[UsersModels.UsersResponse])
async def get_users(session: SessionDep,
                    full_name: str = None,
                    email: str = None,
                    country_code: str = None,
                    phone: str = None,
                    q: str = None,
                    sort: str = "id",
                    order_by: str = "asc",
                    page: int = 1, limit: int = 25):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than or equl to 1")
    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be greater than or equl to 1")

    users = UsersModels.Users
    query = select(users)

    if full_name:
        query = query.where(users.full_name.contains(full_name))
    if email:
        query = query.where(users.email == email)
    if country_code:
        query = query.where(users.country_code == country_code)
    if phone:
        query = query.where(users.phone == phone)
    if q:
        query = query.where((users.full_name.contains(q)) | (users.email.contains(q)))

    order = getattr(users, sort)
    if order_by == "desc":
        order = order.desc()
    query = query.order_by(order)

    query = query.offset((page - 1) * limit).limit(limit)
    return session.exec(query).all()


@router.get("/api/users/{user_id}", tags=["users"], status_code=status.HTTP_200_OK,
            response_model=UsersModels.UsersResponse)
async def get_user(user = Depends(user_exists)):
    return user


@router.post("/api/users", tags=["users"], status_code=status.HTTP_201_CREATED,
             response_model=UsersModels.UserAddedResponse)
async def create_user(user: UsersModels.UserAdd, session: SessionDep):
    salt = "5gz"
    user.password = user.password + salt
    user.password = hashlib.md5(user.password.encode()).hexdigest()

    db_user = UsersModels.Users(**user.model_dump())

    if db_user.phone:
        query = select(UsersModels.Users).where(UsersModels.Users.phone == db_user.phone)
        phone_exists = session.exec(query).first() is not None
        if phone_exists:
            raise HTTPException(status_code=409, detail="Phone is already use")

    if db_user.email:
        query = select(UsersModels.Users).where(UsersModels.Users.email == db_user.email)
        email_exists = session.exec(query).first() is not None
        if email_exists:
            raise HTTPException(status_code=409, detail="Email is already use")

    try:
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'Failed create a user: {err}')
    return db_user
