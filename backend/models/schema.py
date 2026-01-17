from pydantic import BaseModel
from datetime import date
class UserCreate(BaseModel):
    name:str
    email:str
    password:str
    role:str
class loginschema(BaseModel):
    name:str
    password:str
class productschema(BaseModel):
    name:str
    stock:int
    reorder_level:int
    price:int
class Inventorycreate(BaseModel):
    product_id: int
    stock_quantity: int
    reorder_level: int

class SaleCreate(BaseModel):
    product_id: int
    quantity_sold: int
    revenue: float
    sale_date: date