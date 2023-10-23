from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="/applications", tags=["API Keys"], include_in_schema=False)

templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse, name="applications.index")
async def create(request: Request):
    companies = [{"id": 1, "name": "SNAPI Inc.", "registration_number": "234-5673-GH", }]
    applications = [{"id": 1, "name": "MultiPlatform Flutter", "created_at": "2023-06-11", }]
    return templates.TemplateResponse("pages/applications/index.html",
                                      {"request": request, "applications": applications, "companies": companies, })


@router.post("/create", response_class=HTMLResponse)
async def store_apikey(request: Request):
    return templates.TemplateResponse("pages/applications/create.html", {"request": request, "message": "Success"})


@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id.desc())
    return templates.TemplateResponse("index.html", {"request": request, "users": users})


@app.post("/add")
async def add(request: Request, name: str = Form(...), position: str = Form("User21"), office: str = Form("Active"),
              db: Session = Depends(get_db)):
    print(name)
    print(position)
    print(office)

    created_at = datetime.now()  # Get the current timestamp
    users = models.User(name=name, position=position, office=office, created_at=created_at)
    db.add(users)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/addnew")
async def addnew(request: Request):
    return templates.TemplateResponse("addnew.html", {"request": request})


@app.get("/edit/{user_id}")
async def edit(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "user": user})


@app.post("/update/{user_id}")
async def update(request: Request, user_id: int, name: str = Form(...), position: str = Form(...),
                 office: str = Form(...), db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == user_id).first()
    users.name = name
    users.position = position
    users.office = office
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, db: Session = Depends(get_db)):
    users = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(users)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)