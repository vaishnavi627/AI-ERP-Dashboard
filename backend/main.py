from fastapi import FastAPI
from database.db import engine,Base
from routes.auths import router
from database.db import UPLOAD_DIR
import os
app = FastAPI()
app.include_router(router)
Base.metadata.create_all(bind=engine)
os.makedirs(UPLOAD_DIR,exist_ok=True)