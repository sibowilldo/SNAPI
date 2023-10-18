from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/companies", tags=["Companies"], include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, name="companies.index")
async def create(request: Request):
    companies = [{"id": 1, "name": "SNAPI Inc.", "registration_number": "234-5673-GH", }]
    applications = [{"id": 1, "name": "MultiPlatform Flutter", "created_at": "2023-06-11", }]

    return templates.TemplateResponse("pages/companies/index.html",
                                      {"request": request, "applications": applications, "companies": companies, })


@router.post("/create", response_class=HTMLResponse)
async def store_apikey(request: Request):
    return templates.TemplateResponse("pages/companies/create.html", {"request": request, "message": "Success"})
