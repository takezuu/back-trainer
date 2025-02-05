from sqlalchemy import Column, Integer, String, DATETIME
from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String, index=True)
    ip_address = Column(String, index=True)
    created_at = Column(DATETIME, index=True)
    last_login_time = Column(String, index=True)
    country_code = Column(String, index=True)
    phone = Column(String, index=True)


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    address = Column(String, index=True)
    contact_phone = Column(String, index=True)
    date_of_birth = Column(DATETIME, index=True)
