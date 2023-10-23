from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session
from starlette import status
from starlette.responses import RedirectResponse

from app import models
from app import repository as repo
from app.database.database import get_db
from app.schema import ApplicationCreate, ApplicationUpdate

router = APIRouter(prefix="/applications", tags=["Applications"], include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, name="applications.index")
async def index(request: Request, db: Session = Depends(get_db)):
    applications = repo.get_applications_by_company_ids(db=db, ids=[1])
    return templates.TemplateResponse("pages/applications/index.html",
                                      {"request": request, "applications": applications})


@router.get("/create", response_class=HTMLResponse, name="applications.create")
async def create(request: Request, db: Session = Depends(get_db)):
    companies = repo.get_companies(db=db, user_id=1).all()  # Todo: Get this from logged in user
    return templates.TemplateResponse("pages/applications/create.html",
                                      {"request": request, "companies": companies})


@router.post("/store", response_class=HTMLResponse, name="applications.store")
async def store(request: Request, application_name: Annotated[str, Form()],
                company_id: Annotated[int, Form()], db: Session = Depends(get_db)):
    application = repo.create_application(db=db,
                                          application=ApplicationCreate(name=application_name, company_id=company_id,
                                                                        status_id=1))
    return RedirectResponse(url=router.url_path_for("applications.index"), status_code=status.HTTP_303_SEE_OTHER)


@router.get("/edit/{application_id}", response_class=HTMLResponse, name="applications.edit")
async def edit(request: Request, application_id: int, db: Session = Depends(get_db)):
    application = repo.get_application_by_id(db=db, application_id=application_id)
    companies = repo.get_companies(db=db, user_id=1)  # ToDo: Get from logged in user
    statuses = repo.get_statuses(db=db)

    return templates.TemplateResponse("pages/applications/edit.html",
                                      {"request": request, "application": application, "companies": companies,
                                       "statuses": statuses})

