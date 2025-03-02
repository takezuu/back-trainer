from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from src.dependencies.items import item_exists
from src.database import get_session
from src.models.items import Items, ItemAdd, ItemAddedResponse, ItemUpdatedResponse, ItemsPatch

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()




@router.get("/api/items", tags=["items"], response_model=List[Items])
async def get_items(session: SessionDep,
                    product_name: str = None,
                    price: float = None,
                    category: str = None,
                    item_color: str = None,
                    rating: int = None,
                    q: str = None,
                    ge_rating: int = None,
                    le_rating: int = None,
                    ge_price: int = None,
                    le_price: int = None,
                    sort: str = "id",
                    order_by: str = "asc",
                    page: int = 1,
                    limit: int = 25
                    ):
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than or equl to 1")
    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be greater than or equl to 1")

    items = Items
    query = select(items)

    if product_name:
        query = query.where(items.product_name == product_name)
    if price:
        query = query.where(items.price == price)
    if category:
        query = query.where(items.category == category)
    if item_color:
        query = query.where(items.item_color == item_color)
    if rating:
        query = query.where(items.rating == rating)
    if ge_price:
        query = query.where(items.price >= ge_price)
    if le_price:
        query = query.where(items.price <= le_price)
    if ge_rating:
        query = query.where(items.rating >= ge_rating)
    if le_rating:
        query = query.where(items.rating <= le_rating)
    if q:
        query = query.where(
            (items.description.contains(q)) | (items.category.contains(q)) | (items.item_color.contains(q)) | (
                items.product_name.contains(q)))

    order = getattr(items, sort)
    if order_by == "desc":
        order = order.desc()
    query = query.order_by(order)

    query = query.offset((page - 1) * limit).limit(limit)
    return session.exec(query).all()


@router.get("/api/items/{item_id}", tags=["items"], response_model=Items)
async def get_item(item=Depends(item_exists)):
    return item



@router.post("/api/items", tags=["items"], status_code=status.HTTP_201_CREATED,
             response_model=ItemAddedResponse)
async def create_user(item: ItemAdd, session: SessionDep):
    db_item = Items(**item.model_dump())

    if db_item.product_name:
        query = select(Items).where(Items.product_name == db_item.product_name)
        product_name_exists = session.exec(query).first() is not None
        if product_name_exists:
            raise HTTPException(status_code=409, detail="Product name is already use")

    try:
        session.add(db_item)
        session.commit()
        session.refresh(db_item)
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=500, detail=f'Failed create an item: {err}')
    return db_item

@router.delete("/api/items/{item_id}", tags=["items"], status_code=status.HTTP_200_OK)
async def delete_item(session: SessionDep, item=Depends(item_exists)):
    try:
        session.delete(item)
        session.commit()
        return {"message": "Item deleted successfully"}
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

@router.patch("/api/items/{item_id}", tags=["items"], status_code=status.HTTP_200_OK,
              response_model=ItemUpdatedResponse)
async def patch_item(session: SessionDep, update_data: ItemsPatch, item=Depends(item_exists)):
    try:

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)

        session.add(item)
        session.commit()
        session.refresh(item)

        return {"message": "Item updated successfully", "updated_item": item}
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))

@router.put("/api/items/{item_id}", tags=["items"], status_code=status.HTTP_200_OK,
            response_model=ItemUpdatedResponse)
async def put_item(session: SessionDep, update_data: Items, item=Depends(item_exists)):
    try:

        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(item, key, value)

        session.add(item)
        session.commit()
        session.refresh(item)
        return {"message": "Item updated successfully", "updated_item": item}
    except Exception as err:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(err))


