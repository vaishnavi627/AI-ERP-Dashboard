from sqlalchemy import Column,Integer,String,ForeignKey,Date,Float
from database.db import Base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    email = Column(String,unique=True)
    password = Column(String)
    role = Column(String)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer,primary_key=True)
    name = Column(String)
    stock = Column(Integer)
    reorder_level = Column(Integer)
    price = Column(Float)

# class Sales(Base):
    # __tablename__ = "sales"
    # id = Column(Integer,primary_key=True)
    # name = Column(String)
    # product_id = Column(Integer,ForeignKey("products.id"))
    # quantity = Column(Integer)
    # sale_date = Column(Date)

class Inventory(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True)
    stock_quantity = Column(Integer, nullable=False)
    reorder_level = Column(Integer, nullable=False)

    product = relationship("Product")

class Sale(Base):
    __tablename__ = "saless"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity_sold = Column(Integer, nullable=False)
    revenue = Column(Float, nullable=False)
    sale_date = Column(Date, nullable=False)

    product = relationship("Product")