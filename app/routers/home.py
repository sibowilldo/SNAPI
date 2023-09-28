from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from ..utils.auth import oauth2_scheme

router = APIRouter(prefix="", tags=["Home"])

templates = Jinja2Templates(directory="templates")


@router.get("/dashboard", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("pages/dashboard.html", {"request": request})


@router.get("/apikey", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("pages/apikey.html", {"request": request, "logged_in_user": "Sibongiseni"})


@router.get("/changelog")
async def changelog(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"message": "Success", "data": {"v1_0_0": ""}}


@router.get("/login", response_class=HTMLResponse)
async def display_login_page(request: Request):
    return templates.TemplateResponse("pages/auth/login.html", {"request": request})
