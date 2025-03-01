from fastapi import Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from src.models.users import Users


async def user_exists(user_id: int, session: AsyncSession = Depends(get_session)):
    query = select(Users).where(Users.id == user_id)
    user = session.exec(query).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")
