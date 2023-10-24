from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from starlette.templating import Jinja2Templates

from ..utils.auth import oauth2_scheme

router = APIRouter(prefix="", tags=["Home"], include_in_schema=False)

app = FastAPI()

templates: Jinja2Templates = Jinja2Templates(directory="templates")


@router.get("/", name="home")
async def home():
    return {"message": "Silence is Golden!"}


@router.get("/dashboard", response_class=HTMLResponse, name="dashboard")
async def read_item(request: Request):
    return templates.TemplateResponse("pages/dashboard.html", {"request": request})


@router.get("/changelog", name="changelog")
async def changelog(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"message": "Success", "data": {"v1_0_0": ""}}
