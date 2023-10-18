from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models import AccessToken
from app.models import Ability

router = APIRouter(prefix="/api-keys", tags=["API Keys"])

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, name="apikeys.index", include_in_schema=False)
async def list_all(request: Request):
    alert = {"title": "No keys found", "message": "It seems you don't have any keys."}
    return templates.TemplateResponse("pages/api-keys/index.html",
                                      {"request": request,
                                       "alert": alert})


@router.get("/create", response_class=HTMLResponse, name="apikeys.create", include_in_schema=False)
async def create(request: Request, db: Session = Depends(get_db)):
    companies = [{"id": 1, "name": "SNAPI Inc.", "registration_number": "234-5673-GH", }]
    applications = [{"id": 1, "name": "MultiPlatform Flutter", "created_at": "2023-06-11", }]
    abilities = db.query(Ability).filter(Ability.status_id == 1).all()
    return templates.TemplateResponse("pages/api-keys/create.html",
                                      {"request": request, "applications": applications, "companies": companies,
                                       "abilities": abilities})


@router.post("/create", response_class=HTMLResponse, include_in_schema=False)
async def store_apikey(request: Request):
    print(request)
    return templates.TemplateResponse("pages/api-keys/create.html", {"request": request, "message": "Success"})
