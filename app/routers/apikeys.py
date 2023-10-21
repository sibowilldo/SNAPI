from datetime import timedelta
from typing import Annotated, List

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import repository as repo
from app.database.database import get_db
from app.utils.auth import create_access_token

router = APIRouter(prefix="/api-keys", tags=["API Keys"], include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, name="apikeys.index")
async def list_all(request: Request):
    alert = {"title": "No keys found", "message": "It seems you don't have any keys."}
    token = {"token": "sn_7kw378t34rbsfpoiser8723oi_",
             "message": "Make sure you copy this token now. You won't be able to see it again, and we can't recover "
                        "it for you."}
    return templates.TemplateResponse("pages/api-keys/index.html",
                                      {"request": request,
                                       "token": token})


@router.get("/create", response_class=HTMLResponse, name="apikeys.create")
async def create(request: Request, db: Session = Depends(get_db)):
    companies = repo.get_companies(db=db, user_id=1)  # Todo: Get this from logged in user
    abilities = repo.get_abilities(db=db, status_id=1)

    return templates.TemplateResponse("pages/api-keys/create.html",
                                      {"request": request, "companies": companies, "applications": [],
                                       "abilities": abilities})


@router.post("/create", response_class=HTMLResponse, name="apikeys.store", include_in_schema=False)
async def store_apikey(request: Request,
                       company_id: Annotated[int, Form()],
                       application_id: Annotated[int, Form()],
                       abilities: Annotated[List[int], Form()],
                       lifespan: Annotated[int, Form()],
                       db: Session = Depends(get_db),
                       ):
    application = repo.get_application_by_id(db=db, application_id=application_id)

    token = create_access_token({'sub': f'{application.name}', 'scopes': abilities}, timedelta(days=lifespan * 30))

    token_ = {"token": token,
              "message": "Make sure you copy this token now. You won't be able to see it again."}

    return templates.TemplateResponse("pages/api-keys/index.html", {
        "request": request,
        "message": "Success",
        "token": token_
    })
