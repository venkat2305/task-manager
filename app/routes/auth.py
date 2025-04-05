from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..models.user_model import UserCreate, UserInDB, Token
from ..services.auth_service import AuthService

router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate):
    user = await AuthService.create_user(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    return {
        "_id": str(user.user_id),
        "email": user.email,
        "username": user.username,
        "created_at": user.created_at
    }


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await AuthService.authenticate_user(
        email=form_data.username,  # OAuth2 form uses username field for email
        password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AuthService.create_user_token(str(user.user_id))