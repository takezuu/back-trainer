from sqlalchemy import Column, Integer, String
from src.database import Base

class User(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=True, index=True)
    last_name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    city = Column(String, unique=True, index=True)
    shirt_size = Column(String, unique=True, index=True)
