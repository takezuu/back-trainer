from typing import List
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from src import models, routes
from src.database import get_db, engine
from src import schemas

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(routes.router)


@app.get("/")
def root():
    return {"message": "ЗДАРОВААА!!!!"}
