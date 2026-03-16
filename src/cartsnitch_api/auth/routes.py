"""Auth routes: register, login, refresh, me."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from cartsnitch_api.auth.dependencies import get_current_user
from cartsnitch_api.schemas import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(body: RegisterRequest):
    # TODO: call service layer — create user, hash password, return tokens
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest):
    # TODO: call service layer — verify credentials, return tokens
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post("/refresh", response_model=TokenResponse)
async def refresh(body: RefreshRequest):
    # TODO: call service layer — validate refresh token, return new tokens
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.get("/me", response_model=UserResponse)
async def get_me(user_id: UUID = Depends(get_current_user)):
    # TODO: call service layer — fetch user profile
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
