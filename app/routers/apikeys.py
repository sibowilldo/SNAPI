from datetime import timedelta, datetime
from typing import Annotated, List

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import RedirectResponse

from app import repository as repo
from app.database.database import get_db
from app.repository import get_user_access_tokens
from app.schema import AccessTokenCreate
from app.utils.auth import create_access_token

router = APIRouter(prefix="/api-keys", tags=["API Keys"], include_in_schema=False)

templates = Jinja2Templates(directory="templates")


def alert(title: str, message: str) -> dict:
    return {"title": title, "message": message}


@router.get("/", response_class=HTMLResponse, name="apikeys.index")
async def list_all(request: Request, db: Session = Depends(get_db)):
    access_tokens = get_user_access_tokens(db=db, user_id=1)
    return templates.TemplateResponse("pages/api-keys/index.html",
                                      {"request": request, "access_tokens": access_tokens,
                                       "token_count": len(access_tokens)})


@router.get("/create", response_class=HTMLResponse, name="apikeys.create")
async def create(request: Request, db: Session = Depends(get_db)):
    companies = repo.get_companies(db=db, user_id=1).all()  # Todo: Get this from logged in user
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
    access_token = AccessTokenCreate(token=token, application_id=application.id, abilities=abilities,
                                     expires_at=datetime.utcnow() + timedelta(days=lifespan * 30))

    access_tokens = get_user_access_tokens(db=db, user_id=1)

    repo.create_token(db=db, access_token=access_token)

    token_message = {"token": token,
                     "message": """Please save this secret key somewhere safe and accessible. 
                     For security reasons, you won't be able to view it again through your OpenAI account. 
                     If you lose this secret key, you'll need to generate a new one."""}

    return RedirectResponse(url=router.url_path_for('apikeys.index'), status_code=status.HTTP_303_SEE_OTHER)

    # return templates.TemplateResponse("pages/api-keys/index.html", {
    #     "request": request,
    #     "message": "Success",
    #     "token": token_message,
    #     "access_tokens": access_tokens,
    #     "token_count": len(access_tokens)
    # })
