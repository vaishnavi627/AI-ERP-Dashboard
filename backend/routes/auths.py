from fastapi import APIRouter,Depends,HTTPException,UploadFile,File
from sqlalchemy.orm import Session
from models.schema import UserCreate,loginschema,productschema,Inventorycreate
from database.deps import get_db
from models.tables import User,Product,Inventory,Sale
from services.logic import createuser,addproduct,add_inventory,upload_sales_csv
from auth import create_access_token,get_current_user
from services.ai_service import (
    generate_stockout_prediction,
    generate_sales_insights,
    generate_reorder_suggestions,
    generate_weekly_summary
)
router = APIRouter()
@router.post("/createuser")
def create(user:UserCreate,db:Session=Depends(get_db)):
    return createuser(db,user)
@router.get("/getusers")
def display(db:Session=Depends(get_db)):
    return db.query(User).all()
@router.post("/login")
def login(data:loginschema,db:Session=Depends(get_db)):
    user = db.query(User).filter(User.name == data.name,
                                 User.password == data.password).first()
    if not user:
        raise HTTPException(status_code=401,detail="Invalid credentials")
    token  = create_access_token({"email":user.email,"role":user.role})
    return{
        "access_token":token,
        "role":user.role,
        "name":user.name}
@router.post("/product")
def add_product(product:productschema,current_user=Depends(get_current_user),db:Session=Depends(get_db)):
        if current_user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")

        new_product = addproduct(db, product)
        return {
    "message": "Product added successfully",
    "product_id": new_product.id
}
@router.get("/getproduct")
def getusers(db:Session=Depends(get_db)):
    return db.query(Product).all()
@router.post("/addinventory")
def create_inventory(
    data: Inventorycreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return add_inventory(db, data)
@router.get("/getinventory")
def list_inventory(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)):

    if current_user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
    return db.query(Inventory).all()
    
@router.post("/upload")
def upload_sales(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    if current_user["role"] != "admin":
            raise HTTPException(status_code=403, detail="Admin access required")
    return upload_sales_csv(db, file)
@router.get("/sales")
def list_sales(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    
    return db.query(Sale).all()

@router.get("/predict-stockout")
def predict_stockout(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    
    if current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied")

    result = generate_stockout_prediction(db)
    return {
        "status": "success",
        "data": result
    }

@router.get("/predict-stockout")
def predict_stockout(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    
    if current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied")

    result = generate_stockout_prediction(db)
    return {
        "status": "success",
        "data": result
    }
@router.get("/sales-insights")
def sales_insights(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied")

    result = generate_sales_insights(db)
    return {
        "status": "success",
        "data": result
    }


@router.get("/reorder-suggestions")
def reorder_suggestions(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")

    result = generate_reorder_suggestions(db)
    return {
        "status": "success",
        "data": result
    }


@router.get("/weekly-summary")
def weekly_summary(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="Access denied")

    result = generate_weekly_summary(db)
    return {
        "status": "success",
        "data": result
    }