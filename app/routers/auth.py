from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="", tags=["Auth"])

templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def display_login_page(request: Request):
    return templates.TemplateResponse("pages/auth/login.html", {"request": request})
