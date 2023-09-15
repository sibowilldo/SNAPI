from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
from datetime import datetime
from models import Role, User

from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


User.metadata.create_all(bind=engine)


templates = Jinja2Templates(directory="templates")



@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.id.desc).all()
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

@app.get("/create")
async def create(
    request: Request,
    name: str = Form(...),
    registration_no: int = Form(...),
    ContactNo: int = Form(...),
    CreatedAt: datetime = Form(...),
    updatedAt: datetime = Form(...),
    User_id: int = Form(...),
    db: Session = Depends(get_db)
):
    
    user = User(
        name=name,
        registration_no=registration_no,
        ContactNo=ContactNo,
        CreatedAt=CreatedAt,
        updatedAt=updatedAt,
    )
    
    
    role = db.query(Role).filter(User.id == User_id).first()
    if role:
        user.role = role

    db.add(user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.get("/createnew")
async def createnew(request: Request):
    return templates.TemplateResponse("createnew.html", {"request": request})

@app.post("/edit/{user_id}")
async def edit_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("edit.html", {"request": request, "user": user})


@app.post("/update/{user_id}")
async def update(
    request: Request,
    user_id: int,
    name: str = Form(...),
    registration_no: int = Form(...),
    Contact_no: int = Form(...),
    Created_at: datetime = Form(...),
    updated_at: datetime = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    user.name = name
    user.registration_no = registration_no
    user.ContactNo = Contact_no
    user.CreatedAt = Created_at
    user.updatedAt = updated_at
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

@app.post("/delete/{user_id}")
async def delete(
    request: Request,
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    db.delete(user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

