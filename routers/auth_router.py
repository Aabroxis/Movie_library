from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth import verify_password, create_access_token
from data.models import CreateUser, Token
from services.auth_services import create_user, get_user_by_username

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: CreateUser):
    registering = create_user(user)
    if not registering:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    return {"username": user.username, "role": user.role}

@auth_router.post("/token", response_model = Token)
def login(log_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_username(log_data.username)
    if not user or not verify_password(log_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    token = create_access_token({"sub": user["username"], "role": user["role"]})
    return Token(access_token=token)
    
    