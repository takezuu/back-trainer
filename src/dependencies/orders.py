from fastapi import Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database import get_session
from src.models.orders import OrdersModels


async def order_exists(order_id: int, session: AsyncSession = Depends(get_session)):
    query = select(OrdersModels.Orders).where(OrdersModels.Orders.id == order_id)
    order = session.exec(query).first()
    if order:
        return order
    raise HTTPException(status_code=404, detail="Order not found")
