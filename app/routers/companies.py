from fastapi import APIRouter, Request, Depends, Form, HTTPException, Cookie
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

from app import repository
from app.database.database import get_db
from app.models import Company
from app.schema import CompanyCreate, AddressCreate

router = APIRouter(prefix="/companies", tags=["Companies"], include_in_schema=False)

templates = Jinja2Templates(directory="templates")

countries = ['South Africa']
provinces = ['Eastern Cape', 'Free State', 'Gauteng', 'Limpopo', 'KwaZulu-Natal', 'Mpumalanga', 'North West',
             'Northern Cape', 'Western Cape']


@router.get("/", name="companies.index")
async def home(request: Request, db: Session = Depends(get_db)):
    companies = db.query(Company).order_by(Company.id.asc()).all()
    return templates.TemplateResponse("pages/companies/index.html", {"request": request, "companies": companies})


@router.get("/create", name="companies.create")
async def create_company(request: Request, db: Session = Depends(get_db)):
    user_id = 1

    return templates.TemplateResponse("pages/companies/create.html",
                                      {"request": request, "user_id": user_id, "countries": countries,
                                       "provinces": provinces})


@router.post("/create", name="companies.store")
async def store_company(
        request: Request,
        company: CompanyCreate,
        address: AddressCreate,
        db: Session = Depends(get_db)
):
    try:
        user_id = 1  # Todo: Get from logged in user
        company = repository.create_company(db=db, user_id=user_id, company=company)
        address = repository.create_address(db=db, company_id=company.id, address=address)

        return RedirectResponse(url=router.url_path_for("companies.index"), status_code=status.HTTP_303_SEE_OTHER)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/{company_id}/edit", name="companies.edit")
async def edit_company(request: Request, company_id: int, db: Session = Depends(get_db)):
    company = repository.get_company_by_id(db=db, company_id=company_id)
    return templates.TemplateResponse("pages/companies/edit.html",
                                      {"request": request, "company": company, "countries": countries,
                                       "provinces": provinces})
