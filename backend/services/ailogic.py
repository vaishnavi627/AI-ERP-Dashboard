# services/logic.py

from models.tables import Inventory, Sale
from datetime import date, timedelta

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
def prepare_sales_ai_data(db):
    sales = db.query(Sale).all()

    result = []
    for s in sales:
        result.append({
            "product_id": s.product_id,
            "quantity_sold": s.quantity_sold,
            "revenue": s.revenue,
            "sale_date": str(s.sale_date)
        })

    return result
