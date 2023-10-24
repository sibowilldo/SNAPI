from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schema import UserBase
from app.utils.auth import Token, authenticate_user, create_access_token, get_active_logged_in_user
from app.utils.dependencies import get_api_version

router = APIRouter(prefix=get_api_version(), tags=["Auth"])

