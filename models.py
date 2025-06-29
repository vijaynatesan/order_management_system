
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    zip_code = Column(String)

    orders = relationship("ItemOrder", back_populates="customer")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    manufacturer_name = Column(String)
    manufacturer_email = Column(String)
    in_stock = Column(Integer)
    reorder_quantity = Column(Integer)

    orders = relationship("ItemOrder", back_populates="item")
    reorder_logs = relationship("ItemReorderLog", back_populates="item")

class ItemOrder(Base):
    __tablename__ = "item_orders"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    customer_id = Column(Integer, ForeignKey("customers.id"))
    order_quantity = Column(Integer)

    item = relationship("Item", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")

class ItemReorderLog(Base):
    __tablename__ = "item_reorder_logs"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    item = relationship("Item", back_populates="reorder_logs")
