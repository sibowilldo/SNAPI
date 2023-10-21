from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app import repository as repo, schema
from app.database.database import get_db

router = APIRouter(prefix="/json", tags=["Non-API JSON Responses"], include_in_schema=True)


@router.get("/companies/{company_id}/applications", response_model=list[schema.Application],
            name="json.companies.applications")
async def create(company_id: int, db: Session = Depends(get_db)):
    return repo.get_applications_by_company_id(db=db, company_id=company_id)
