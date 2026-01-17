from jose import jwt
from datetime import datetime, timedelta
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
SECRET_KEY = "secret123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#This tells FastAPI where token comes from
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM]) #it contain decoded values email and role
        email = payload.get("email")
        role = payload.get("role")

        if email is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token payload")
        return {
            "email":email,
            "role":role
        }
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail = "Token is invalid or expired")
    
