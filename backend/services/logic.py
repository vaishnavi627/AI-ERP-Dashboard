from models.tables import User,Product,Inventory,Sale
import pandas as pd
from datetime import date, timedelta

def createuser(db,userdata):
    new_user = User(name=userdata.name,email=userdata.email,password=userdata.password,role=userdata.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return "data added successfully"
def addproduct(db,product):
    new_product = Product(
        name=product.name,
        stock=product.stock,
        reorder_level=product.reorder_level,
        price=product.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

def add_inventory(db, data):
    inventory = Inventory(
        product_id=data.product_id,
        stock_quantity=data.stock_quantity,
        reorder_level=data.reorder_level
    )
    db.add(inventory)
    db.commit()
    db.refresh(inventory)
    return inventory

def upload_sales_csv(db, file):
    file.file.seek(0)

    df = pd.read_csv(file.file, encoding="utf-8-sig")
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace("\ufeff", "")
    )

    print("CSV columns:", df.columns.tolist())
    print(df.head())

    for _, row in df.iterrows():
        sale = Sale(
            product_id=int(row["product_id"]),
            quantity_sold=int(row["quantity_sold"]),
            revenue=float(row["revenue"]),
            sale_date=pd.to_datetime(row["sale_date"]).date()
        )

        db.add(sale)

    db.commit()
    return {"message": "Sales data uploaded successfully"}

def prepare_inventory_ai_data(db):
    inventory = db.query(Inventory).all()
    sales = db.query(Sale).all()

    data = []

    for item in inventory:
        product_sales = [s for s in sales if s.product_id == item.product_id]
        total_sold = sum(s.quantity_sold for s in product_sales)

        data.append({
            "product": item.product.name,
            "current_stock": item.stock_quantity,
            "reorder_level": item.reorder_level,
            "total_units_sold": total_sold
        })

    return data
def prepare_weekly_sales_data(db):
    last_week = date.today() - timedelta(days=7)

    sales = db.query(Sale).filter(
        Sale.sale_date >= last_week
    ).all()

    return [{
        "product": s.product.name,
        "quantity_sold": s.quantity_sold,
        "revenue": s.revenue
    } for s in sales]