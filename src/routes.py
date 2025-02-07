from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.database import get_db
from src import schemas, models

router = APIRouter()


@router.get("/users", tags=["users"], response_model=List[schemas.User])
async def read_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/customers", tags=["customers"], response_model=List[schemas.Customer])
async def read_users(db: Session = Depends(get_db)):
    customer = db.query(models.Customer).all()
    return customer


@router.get("/orders", tags=["orders"], response_model=List[schemas.Order])
async def read_users(db: Session = Depends(get_db)):
    customer = db.query(models.Order).all()
    return customer

@router.get("/items", tags=["items"], response_model=List[schemas.Item])
async def read_users(db: Session = Depends(get_db)):
    customer = db.query(models.Item).all()
    return customer
