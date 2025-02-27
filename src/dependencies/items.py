from fastapi import Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import get_session
from src.models.items import ItemsModels


async def item_exists(item_id: int, session: AsyncSession = Depends(get_session)):
    query = select(ItemsModels.Items).where(ItemsModels.Items.id == item_id)
    item = session.exec(query).first()
    if item:
        return item
    raise HTTPException(status_code=404, detail="Item not found")
