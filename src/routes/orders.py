from datetime import datetime
from typing import List, Annotated
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session, select

from src.dependencies.orders import order_exists
from src.models.items import Items
from src.models.orders import Orders, OrderAddedResponse, OrderAdd, OrderPut, OrderUpdatedResponse, \
    OrderPatch, OrderResponse, OrdersResponse
from src.database import get_session
from src.models.users import Users

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/api/orders", tags=["orders"], response_model=List[OrdersResponse])
async def get_orders(session: SessionDep,
                     order_date_time: datetime = None,
                     discount: float = None,
                     total_amount: float = None,
                     delivery_address: str = None,
                     item_id: int = None,
                     sort: str = "id",
                     order_by: str = "asc",
                     page: int = 1,
                     limit: int = 25
                     ):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than or equl to 1")
    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be greater than or equl to 1")

    orders = Orders
    query = select(orders)

    if order_date_time:
        query = query.where(orders.order_date == order_date_time)
    if discount:
        query = query.where(orders.discount == discount)
    if total_amount:
        query = query.where(orders.total_amount == total_amount)
    if delivery_address:
        query = query.where(orders.delivery_address == delivery_address)
    if item_id:
        query = query.where(orders.items_ids.contains([item_id]))

    order = getattr(orders, sort)
    if order_by == "desc":
        order = order.desc()
    query = query.order_by(order)

    query = query.offset((page - 1) * limit).limit(limit)

    orders = session.exec(query).all()
    for order in orders:
        if order.order_date:
            order.order_date = order.order_date.strftime("%Y-%m-%d %H:%M:%S")

    return orders


@router.get("/api/orders/{order_id}", tags=["orders"], response_model=OrderResponse)
async def get_order(session: SessionDep, order=Depends(order_exists)):
    if order.order_date:
        order.order_date = order.order_date.strftime("%Y-%m-%d %H:%M:%S")

    items_data = []
    for item_id in order.items_ids:
        items = Items
        query = select(items).where(items.id == item_id)
        item = session.exec(query).first()
        if item:
            item = item.model_dump()
            items_data.append(item)

    del order.items_ids  # delete old field
    order = order.model_dump()
    order["items"] = items_data  # recreate new

    return order


@router.post("/api/orders", tags=["orders"], status_code=status.HTTP_201_CREATED,
             response_model=OrderAddedResponse)
async def create_order(order: OrderAdd, session: SessionDep):
    query = select(Users).where(Users.id == order.user_id)
    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    order.order_date = datetime.now().replace(microsecond=0)

    if not order.items_ids:
        raise HTTPException(status_code=400, detail="Items array should have at least one element")

    total_price = 0
    for item_id in order.items_ids:
        item_quantity_in_items_ids = order.items_ids.count(item_id)
        query = select(Items).where(Items.id == item_id)
        item = session.exec(query).first()
        if item.price is None:
            raise HTTPException(status_code=404, detail=f"Item not found id:{item_id}")

        if item.quantity < item_quantity_in_items_ids:
            raise HTTPException(status_code=404,
                                detail=f"Requested quantity for item with ID {item_id} in the order exceeds the available stock in the warehouse")
        item.quantity -= item_quantity_in_items_ids

        try:
            session.add(item)
            session.commit()
            session.refresh(item)
        except Exception as err:
            session.rollback()
            raise HTTPException(status_code=500, detail=f'Update item quantity: {err}')

        total_price += item.price
    order_discount = total_price * (order.discount / 100)
    total_price = total_price - order_discount

    order.total_amount = total_price
    db_order = Orders(**order.model_dump())

    try:
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'Failed create an order: {err}')
    return db_order


@router.delete("/api/orders/{order_id}", tags=["orders"], status_code=status.HTTP_200_OK)
async def delete_order(session: SessionDep, order=Depends(order_exists)):
    try:
        session.delete(order)
        session.commit()
        return {"message": "Order deleted successfully"}
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


@router.patch("/api/orders/{order_id}", tags=["orders"], status_code=status.HTTP_200_OK,
              response_model=OrderUpdatedResponse)
async def patch_order(session: SessionDep, update_data: OrderPatch, order=Depends(order_exists)):
    try:

        if update_data.discount is None:
            discount = order.discount
        else:
            discount = update_data.discount

        if update_data.items_ids is None:
            items_ids = order.items_ids
        else:
            items_ids = update_data.items_ids

        old_items_dict = {f"{item_id}": order.items_ids.count(item_id) for item_id in order.items_ids}
        curent_items_dict = {f"{item_id}": items_ids.count(item_id) for item_id in items_ids}
        zipped_dict = old_items_dict | curent_items_dict

        if update_data.discount is not None or update_data.items_ids is not None:
            total_price = 0
            for item_id in zipped_dict.keys():
                item_id = int(item_id)
                item_quantity_in_items_ids = items_ids.count(item_id)
                query = select(Items).where(Items.id == item_id)
                item = session.exec(query).first()

                if item is None and str(item_id) in curent_items_dict:
                    raise HTTPException(status_code=404, detail=f"Item not found id:{item_id}")
                elif item is None and str(item_id) in old_items_dict:
                    continue

                if str(item_id) in old_items_dict:
                    old_value = old_items_dict[f"{item_id}"]
                else:
                    old_value = 0

                if old_value > item_quantity_in_items_ids:
                    difference = old_value - item_quantity_in_items_ids
                    item.quantity += difference

                elif old_value < item_quantity_in_items_ids:
                    if item.quantity == 0:
                        raise HTTPException(status_code=404,
                                            detail=f"Requested quantity for item with ID {item_id} in the order exceeds the available stock in the warehouse")
                    difference = item_quantity_in_items_ids - old_value
                    available = item.quantity
                    item.quantity -= difference
                    if item.quantity <= 0:
                        raise HTTPException(status_code=404,
                                            detail=f"Requested quantity for item with ID {item_id} in the order exceeds the available stock: {available} in the warehouse")

                try:
                    session.add(item)
                    session.commit()
                    session.refresh(item)
                except Exception as err:
                    session.rollback()
                    raise HTTPException(status_code=500, detail=f'Update item quantity: {err}')

                total_price += item.price
            order_discount = total_price * (discount / 100)
            total_price = total_price - order_discount
            update_data.total_amount = total_price
        update_data = Orders(**update_data.model_dump())

        for key, value in update_data.model_dump(exclude_unset=True).items():
            if value is not None:
                setattr(order, key, value)
        session.add(order)
        session.commit()
        session.refresh(order)
        if order.order_date:
            order.order_date = order.order_date.strftime("%Y-%m-%d %H:%M:%S")
        return {"message": "Order updated successfully", "updated_order": order}
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


@router.put("/api/orders/{order_id}", tags=["orders"], status_code=status.HTTP_200_OK,
            response_model=OrderUpdatedResponse)
async def put_order(session: SessionDep, update_data: OrderPut, order=Depends(order_exists)):
    try:
        old_items_dict = {f"{item_id}": order.items_ids.count(item_id) for item_id in order.items_ids}
        curent_items_dict = {f"{item_id}": update_data.items_ids.count(item_id) for item_id in update_data.items_ids}
        zipped_dict = old_items_dict | curent_items_dict

        if not update_data.items_ids:
            raise HTTPException(status_code=400, detail="Items array should have at least one element")
        total_price = 0
        for item_id in zipped_dict.keys():
            item_id = int(item_id)
            item_quantity_in_items_ids = order.items_ids.count(item_id)
            query = select(Items).where(Items.id == item_id)
            item = session.exec(query).first()

            if item is None and str(item_id) in curent_items_dict:
                raise HTTPException(status_code=404, detail=f"Item not found id:{item_id}")
            elif item is None and str(item_id) in old_items_dict:
                continue

            if str(item_id) in old_items_dict:
                old_value = old_items_dict[f"{item_id}"]
            else:
                old_value = 0

            if old_value > item_quantity_in_items_ids:
                difference = old_value - item_quantity_in_items_ids
                item.quantity += difference

            elif old_value < item_quantity_in_items_ids:
                difference = item_quantity_in_items_ids - old_value
                item.quantity -= difference


            elif old_value < item_quantity_in_items_ids:
                if item.quantity == 0:
                    raise HTTPException(status_code=404,
                                        detail=f"Requested quantity for item with ID {item_id} in the order exceeds the available stock in the warehouse")
                difference = item_quantity_in_items_ids - old_value
                available = item.quantity
                item.quantity -= difference

                if item.quantity <= 0:
                    raise HTTPException(status_code=404,
                                        detail=f"Requested quantity for item with ID {item_id} in the order exceeds the available stock: {available} in the warehouse")

            try:
                session.add(item)
                session.commit()
                session.refresh(item)
            except Exception as err:
                session.rollback()
                raise HTTPException(status_code=500, detail=f'Update item quantity: {err}')

            total_price += item.price

            try:
                session.add(item)
                session.commit()
                session.refresh(item)
            except Exception as err:
                session.rollback()
                raise HTTPException(status_code=500, detail=f'Update item quantity: {err}')

        order_discount = total_price * (update_data.discount / 100)
        total_price = total_price - order_discount

        update_data.total_amount = total_price
        update_data = Orders(**update_data.model_dump())

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(order, key, value)

        session.add(order)
        session.commit()
        session.refresh(order)

        if order.order_date:
            order.order_date = order.order_date.strftime("%Y-%m-%d %H:%M:%S")
        return {"message": "Order updated successfully", "updated_order": order}
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))
