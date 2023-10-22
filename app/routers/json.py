from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette import status

from app import repository as repo, schema
from app.database.database import get_db

router = APIRouter(prefix="/json", tags=["Non-API JSON Responses"], include_in_schema=True)


@router.get("/companies/{company_id}/applications", response_model=list[schema.Application],
            name="json.companies.applications")
async def create(company_id: int, db: Session = Depends(get_db)):
    return repo.get_applications_by_company_id(db=db, company_id=company_id)


@router.delete("/apikeys/{access_token_id}", name="apikeys.delete")
async def delete_api_key(access_token_id: int, db: Session = Depends(get_db)):
    message = "Access Token deleted"
    response = repo.delete_token(db=db, access_token_id=access_token_id)
    if response == 0:
        raise HTTPException(detail='Failed to delete token.', status_code=status.HTTP_400_BAD_REQUEST)
    return {"message": message, "response": response}, 200
