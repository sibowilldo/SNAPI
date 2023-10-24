from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ..schema import UserBase
from ..utils.auth import Token, authenticate_user, create_access_token, get_active_logged_in_user
from ..utils.dependencies import get_api_version
from ..utils.fake_db import fake_users_db

router = APIRouter(prefix=get_api_version(), tags=["Auth"])

ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": f"{user.username}"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/user", response_model=UserBase)
async def read_auth_user(logged_in_user: Annotated[str, Depends(get_active_logged_in_user)]):
    return logged_in_user
