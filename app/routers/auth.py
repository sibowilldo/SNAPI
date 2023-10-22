from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.routers.home import app

router = APIRouter(prefix="", tags=["Auth"])

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def display_login_page(request: Request):
    return templates.TemplateResponse("pages/auth/login.html", {"request": request})


@app.get("/login")
def home(request: Request):
    return templates.TemplateResponse("pages/auth/login.html", {"request": request})


@app.get("/register")
def signup(request: Request):
    return templates.TemplateResponse("pages/auth/register.html", {"request": request})


@app.get("/reset/password")
def reset_password(request: Request):
    return templates.TemplateResponse("pages/auth/reset_password.html", {"request": request})


# In-memory database for storing reset tokens (use a real database in production)
reset_tokens = {}


@app.get("/reset-email")
async def reset_email(request: Request):
    return templates.TemplateResponse("email_template.html", {"request": request, "reset_link": "your_reset_link_here"})


@app.post("/reset-password")
async def reset_password(request: Request, password: str = Form(...), token: str = Form(...)):
    if token in reset_tokens and reset_tokens[token] == "user_id":
        # Reset the user's password here (e.g., update it in a database)
        return {"message": "Password reset successfully"}
    return {"message": "Invalid or expired token"}


class EmailForm(BaseModel):
    email: str


@app.post("/validate-email/", response_class=HTMLResponse)
async def validate_email(request: Request, form: EmailForm):
    email = form.email
    is_valid = validate_email_format(email)  # Your email validation function

    return templates.TemplateResponse("pages/auth/emailvalidation.html", {"request": request, "is_valid": is_valid, "email": email})


def validate_email_format(email):
    # Implement your email validation logic here
    # You can use regular expressions or any other method
    # For a simple example, we check for "@" in the email
    if "@" in email:
        return True
    return False
