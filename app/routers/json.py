from fastapi import APIRouter, Depends, HTTPException, Response, Request, Form
from sqlalchemy.orm import Session
from starlette import status

from app import repository as repo, schema
from app.database.database import get_db
from app.schema import ApplicationUpdate, CompanyUpdate, AddressUpdate

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
    return {"message": message, "response": response}


@router.delete("/applications/{application_id}", name="applications.destroy")
async def delete_application(application_id: int, db: Session = Depends(get_db), response: Response = 200):
    message = "Application has been deleted"
    delete_response = repo.delete_application(db=db, application_id=application_id)
    if response == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(detail='Failed to delete Application.', status_code=status.HTTP_400_BAD_REQUEST)
    response.status_code = status.HTTP_200_OK
    return {"message": message, "response": delete_response}


@router.patch("/applications/{application_id}/update", name="applications.update")
async def update_application(
        application_id: int,
        application: ApplicationUpdate,
        db: Session = Depends(get_db), response: Response = 200):
    application = repo.update_application(db=db, application=application)
    response.status_code = status.HTTP_202_ACCEPTED
    return {"message": f'{application.name} updated, successfully.', "application": application}


@router.delete("/delete/{company_id}", name="companies.delete")
async def delete_company(
        request: Request,
        company_id: int,
        db: Session = Depends(get_db), response: Response = 200
):
    message = "Company has been deleted"
    delete_response = repo.delete_company(db=db, company_id=company_id)
    if response == 0:
        response.status_code = status.HTTP_400_BAD_REQUEST
        raise HTTPException(detail='Failed to delete Company.', status_code=status.HTTP_400_BAD_REQUEST)
    response.status_code = status.HTTP_200_OK
    return {"message": message, "response": delete_response}


@router.put("/companies/{company_id}/update", name="companies.update")
async def update_company(
        request: Request,
        company_id: int,
        company: CompanyUpdate,
        db: Session = Depends(get_db),
        response: Response = 200
):
    company = repo.update_company(db=db, company_id=company_id, company=company)
    response.status_code = status.HTTP_202_ACCEPTED
    return {"message": f'{company.name} updated, successfully.', "company": company}
