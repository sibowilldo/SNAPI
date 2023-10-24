from datetime import timedelta
from typing import Optional, List, Annotated

from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

from app.database.database import get_db
from app.schema import UserBase
from app.utils.auth import authenticate_user, create_access_token, get_active_logged_in_user, Token

router = APIRouter(prefix="", tags=["Auth"])

templates = Jinja2Templates(directory="templates")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get(
            "email"
        )
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append("Email is required")
        if not self.password or not len(self.password) >= 4:
            self.errors.append("A valid password is required")
        if not self.errors:
            return True
        return False


@router.get("/login", response_class=HTMLResponse)
async def display_login_page(request: Request):
    return templates.TemplateResponse("pages/auth/login.html", {"request": request})


@router.post("/login")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("pages/auth/login.html", form.__dict__)
            await login_for_access_token(form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("pages/auth/login.html", form.__dict__)
    return templates.TemplateResponse("pages/auth/login.html", form.__dict__)


@router.get("/register")
def signup(request: Request):
    return templates.TemplateResponse("pages/auth/register.html", {"request": request})


@router.get("/reset/password")
def reset_password(request: Request):
    return templates.TemplateResponse("pages/auth/reset_password.html", {"request": request})


# In-memory database for storing reset tokens (use a real database in production)
reset_tokens = {}


@router.get("/reset-email")
async def reset_email(request: Request):
    return templates.TemplateResponse("email_template.html", {"request": request, "reset_link": "your_reset_link_here"})


@router.post("/reset-password")
async def reset_password(request: Request, password: str = Form(...), token: str = Form(...)):
    if token in reset_tokens and reset_tokens[token] == "user_id":
        # Reset the user's password here (e.g., update it in a database)
        return {"message": "Password reset successfully"}
    return {"message": "Invalid or expired token"}


class EmailForm(BaseModel):
    email: str


@router.post("/validate-email/", response_class=HTMLResponse)
async def validate_email(request: Request, form: EmailForm):
    email = form.email
    is_valid = validate_email_format(email)  # Your email validation function

    return templates.TemplateResponse("pages/auth/emailvalidation.html",
                                      {"request": request, "is_valid": is_valid, "email": email})


def validate_email_format(email):
    # Implement your email validation logic here
    # You can use regular expressions or any other method
    # For a simple example, we check for "@" in the email
    if "@" in email:
        return True
    return False


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    user = authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": f"{user.email}"}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/user", response_model=UserBase)
async def read_auth_user(logged_in_user: Annotated[str, Depends(get_active_logged_in_user)]):
    return logged_in_user
