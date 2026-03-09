from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from config import settings
from data.models import TokenData

password_content = CryptContext(schemes=["bcrypt"], deprecated= "auto")
oauth2_shema = OAuth2PasswordBearer(tokenUrl="/auth/token")

def hash_passowrd(password: str): #str
    return password_content.hash(password)

def verify_password(users_pass: str, hashed: str): #bool
    return password_content.verify(users_pass, hashed)

def create_access_token(data: dict): #str
    encoding = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_TIME_LIMIT_MINUTES)
    encoding["exp"] = expire
    return jwt.encode(encoding, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def get_current_user(token: str = Depends(oauth2_shema)): #TokenData
    try:
        decoding = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str  = decoding.get("sub")
        role: str = decoding.get("role")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your token is invalid")
        return TokenData(username=username, role=role)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Your token is invalid")
    
def admin_required(curr_user: TokenData = Depends(get_current_user)): #TokenData
    if curr_user.role != "ADMIN":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="ADMIN access only")
    return curr_user

def user_required(curr_user: TokenData = Depends(get_current_user)): #TokenData
    return curr_user