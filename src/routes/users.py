from typing import List, Optional, Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from src.models.users import User, UserCreate, UserRead
from src.database import get_session
from passlib.context import CryptContext

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()

@router.get("/api/users", tags=["users"], response_model=List[UserRead])
async def get_users(
    session: SessionDep,
    username: Optional[str] = None,
    email: Optional[str] = None,
    country_code: Optional[str] = None,
    q: Optional[str] = None,
    sort: str = "id",
    order_by: str = "asc",
    page: int = 1,
    limit: int = 25
):
    query = select(User)

    if username:
        query = query.where(User.username == username)
    if email:
        query = query.where(User.email == email)
    if country_code:
        query = query.where(User.country_code == country_code)
    if q:
        query = query.where((User.username.contains(q)) | (User.email.contains(q)))

    order = getattr(User, sort)
    if order_by == "desc":
        order = order.desc()
    query = query.order_by(order)

    query = query.offset((page - 1) * limit).limit(limit)
    users = session.exec(query).all()
    return users

@router.get("/api/users/{user_id}", tags=["users"], response_model=UserRead)
async def get_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

@router.post("/api/users", tags=["users"], response_model=UserRead)
async def create_user(user: UserCreate, session: SessionDep):
    # Проверка уникальности телефона
    phone_exists = session.exec(select(User).where(User.phone == user.phone)).first()
    if phone_exists:
        raise HTTPException(status_code=400, detail="Phone is already in use")

    # Проверка уникальности email
    email_exists = session.exec(select(User).where(User.email == user.email)).first()
    if email_exists:
        raise HTTPException(status_code=400, detail="Email is already in use")

    # Создание нового пользователя с хешированным паролем
    db_user = User(
        username=user.username,
        email=user.email,
        phone=user.phone,
        password_hash=get_password_hash(user.password)  # Хеширование пароля
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user