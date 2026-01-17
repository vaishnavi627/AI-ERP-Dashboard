from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
import os
UPLOAD_DIR = "uploads"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR,"databases.db")
engine = create_engine(f"sqlite:///{DB_PATH}",connect_args={"check_same_thread":False})
Base = declarative_base()
Sessionlocal = sessionmaker(bind=engine,autoflush=False,autocommit=False)
