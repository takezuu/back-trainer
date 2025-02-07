from sqlalchemy import Column, Integer, String, DATETIME, ARRAY, Float, TIMESTAMP

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


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, index=True)
    items_ids = Column(ARRAY(Integer), index=True)
    order_date = Column(TIMESTAMP, index=True)
    discount = Column(Integer, index=True)
    total_amount = Column(Float, index=True)
    status = Column(String, index=True)
    delivery_address = Column(String, index=True)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float, index=True)
    quantity = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    item_color = Column(String, index=True)
    rating = Column(Integer, primary_key=True, index=True)
