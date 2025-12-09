from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from typing import Dict

# Environment variables for secrets
import os
JWT_SECRET = os.getenv("JWT_SECRET", "defaultsecret")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Models
class User(BaseModel):
    email: EmailStr
    password: str

class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Fake database for demonstration purposes
fake_db: Dict[str, UserInDB] = {}

# Router initialization
auth_router = APIRouter()

# Helper functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

# Routes
@auth_router.post("/register", response_model=Token)
async def register(user: User):
    if user.email in fake_db:
        raise HTTPException(status_code=400, detail="User already registered")

    hashed_password = get_password_hash(user.password)
    fake_db[user.email] = UserInDB(email=user.email, hashed_password=hashed_password, password=user.password)

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/login", response_model=Token)
async def login(user: User):
    stored_user = fake_db.get(user.email)
    if not stored_user or not verify_password(user.password, stored_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.post("/logout")
async def logout():
    return {"detail": "Successfully logged out"}

@auth_router.post("/password-recovery")
async def password_recovery(email: EmailStr):
    if email not in fake_db:
        raise HTTPException(status_code=404, detail="User not found")

    # Simulation of email sending (to be replaced with a real email service)
    return {"detail": "Password recovery instructions sent to your email"}