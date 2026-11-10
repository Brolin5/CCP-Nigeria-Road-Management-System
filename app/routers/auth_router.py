from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication & Users"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user account (Citizen, Contractor, Field Inspector, or Road Authority Official).
    """
    return AuthService.register_user(db, user_in)

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user credentials and issue an access token.
    """
    user = AuthService.authenticate_user(db, credentials.username, credentials.password)
    return {
        "access_token": f"nrms_jwt_{user.username}_{user.id}",
        "token_type": "bearer",
        "user": user
    }
