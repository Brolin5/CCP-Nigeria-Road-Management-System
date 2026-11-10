import hashlib
import secrets
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.model import User, Role
from app.schemas.user_schema import UserCreate

def hash_password(password: str) -> str:
    """
    Cryptographic password hashing using PBKDF2-HMAC-SHA256 with salt.
    """
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
    return f"pbkdf2:sha256:100000${salt}${key.hex()}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        parts = hashed_password.split("$")
        if len(parts) != 3:
            return plain_password == hashed_password
        salt = parts[1]
        expected_key = parts[2]
        key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt.encode("utf-8"), 100000)
        return secrets.compare_digest(key.hex(), expected_key)
    except Exception:
        return False

class AuthService:
    @staticmethod
    def register_user(db: Session, user_in: UserCreate) -> User:
        # Check if username or email exists
        if db.query(User).filter(User.username == user_in.username).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken."
            )
        if db.query(User).filter(User.email == user_in.email).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

        # Retrieve Role
        role = db.query(Role).filter(Role.name == user_in.role_name.lower()).first()
        if not role:
            # Fallback to citizen
            role = db.query(Role).filter(Role.name == "citizen").first()
            if not role:
                role = Role(name="citizen", description="General public user")
                db.add(role)
                db.flush()

        user = User(
            username=user_in.username,
            email=user_in.email,
            hashed_password=hash_password(user_in.password),
            full_name=user_in.full_name,
            phone_number=user_in.phone_number,
            organization=user_in.organization
        )
        user.roles.append(role)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
