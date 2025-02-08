from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlmodel import select
from src import schemas, models
from src.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]
router = APIRouter()


@router.get("/orders", tags=["orders"], response_model=List[schemas.Orders])
async def read_users(session: SessionDep):
    customer = session.exec(select(models.Orders)).all()
    return customer


@router.get("/orders/{order_id}", tags=["orders"], response_model=schemas.Orders)
async def read_users(order_id: int, session: SessionDep):
    statement = select(models.Orders).where(models.Orders.id == order_id)
    order = session.exec(statement).first()
    return order

# TODO: username – To search for a user by username: GET /users?username=johndoe
# TODO: email – To filter users by email: GET /users?email=john@example.com
# TODO: country_code – To get users from a specific country: GET /users?country_code=US
# TODO: sort – Defines sorting by a field (e.g., created_at, username): GET /users?sort=created_at
# TODO: order – Specifies ascending (asc) or descending (desc) order: GET /users?sort=created_at&order=desc
# TODO: page – Defines the page number: GET /users?page=2
# TODO: limit – Specifies the number of results per page: GET /users?limit=10
# TODO: q – A general search query for username or email: GET /users?q=john