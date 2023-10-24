import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schema
from .models import Company, Address
from .schema import Application, Status
from .utils.auth import get_hashed_password


def get_statuses(db: Session) -> List[Status]:
    return db.query(models.Status).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schema.UserCreate):
    hashed_password = get_hashed_password(user.password)
    db_user = models.User(name=user.name, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_abilities(db: Session, status_id: int, skip: int = 0, limit: int = -1):
    return db.query(models.Ability).filter(models.Ability.status_id == status_id).offset(skip).limit(limit).all()


def create_application(db: Session, application: schema.ApplicationCreate):
    db_application = models.Application(name=application.name, status_id=application.status_id,
                                        company_id=application.company_id)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application


def create_company(db: Session, user_id: int, company: schema.CompanyCreate):
    db_company = models.Company(user_id=user_id,
                                name=company.name,
                                registration_number=company.registration_number,
                                main_contact_number=company.main_contact_number,
                                secondary_contact_number=company.secondary_contact_number)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def create_address(db: Session, company_id: int, address: schema.AddressCreate):
    db_address = models.Address(street_name=address.street_name,
                                street_number=address.street_number,
                                suburb=address.suburb,
                                city=address.city,
                                province_state=address.province_state,
                                postal_zip_code=address.postal_zip_code,
                                country=address.country,
                                company_id=company_id)
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address


def get_applications(db: Session, skip: int = 0, limit: int = -1):
    return db.query(models.Application).offset(skip).limit(limit).all()


def get_ability_by_id(db: Session, ability_id: int) -> Application:
    return db.query(models.Ability).filter(models.Ability.id == ability_id).first()


def get_application_by_id(db: Session, application_id: int) -> Application:
    return db.query(models.Application).filter(models.Application.id == application_id).first()


def get_applications_by_company_id(db: Session, company_id: int, skip: int = 0, limit: int = -1):
    return db.query(models.Application).filter(models.Application.company_id == company_id).offset(skip).limit(
        limit).all()


def get_applications_by_company_ids(db: Session, ids: List[int], skip: int = 0, limit: int = -1) -> List[Application]:
    return db.query(models.Application).filter(models.Application.company_id.in_(ids)).offset(skip).limit(
        limit).all()


def get_companies(db: Session, user_id: int, skip: int = 0, limit: int = -1):
    return db.scalars(select(models.Company).filter(models.Company.user_id == user_id).offset(skip).limit(limit))


def get_company_by_id(db: Session, company_id: int):
    return db.scalar(select(models.Company).filter(models.Company.user_id == company_id))


def get_user_access_tokens(db: Session, user_id: int):
    company_ids = db.scalars(select(models.Company.id).filter(models.Company.user_id == user_id)).all()
    application_ids = db.scalars(
        select(models.Application.id).filter(models.Application.company_id.in_(company_ids))).all()
    access_tokens = db.scalars(
        select(models.AccessToken).filter(models.AccessToken.application_id.in_(application_ids)).order_by(
            models.AccessToken.created_at.desc())).all()
    return access_tokens


def get_access_token_by_id(db: Session, access_token_id: int):
    return db.query(models.AccessToken).filter(models.AccessToken.id == access_token_id).first()


def create_token(db: Session, access_token: schema.AccessTokenCreate):
    db_access_token = models.AccessToken(token=access_token.token, application_id=access_token.application_id,
                                         expires_at=access_token.expires_at)

    for a in access_token.abilities:
        ability = get_ability_by_id(db=db, ability_id=a)
        db_access_token.abilities.append(ability)

    db.add(db_access_token)
    db.commit()
    db.refresh(db_access_token)
    return db_access_token


def delete_token(db: Session, access_token_id: int):
    db_access_token = db.query(models.AccessToken).filter(models.AccessToken.id == access_token_id).delete()
    db.commit()

    return db_access_token


def delete_application(db: Session, application_id: int):
    db_application = db.query(models.Application).filter(models.Application.id == application_id).delete()
    db.commit()


def delete_company(db: Session, company_id: int):
    db_company = db.query(models.Company).filter(models.Company.id == company_id).delete()
    db.commit()

    return db_company


def update_application(db: Session, application: schema.ApplicationUpdate):
    db_application = db.query(models.Application).filter(models.Application.id == application.application_id).first()

    db_application.name = application.name
    db_application.company_id = application.company_id
    db_application.status_id = application.status_id
    db_application.updated_at = datetime.datetime.now()

    db.commit()
    db.refresh(db_application)
    return db_application


def update_company(db: Session, company_id: int, company: schema.CompanyUpdate):
    db_company: Company = db.query(models.Company).filter(models.Company.id == company_id).first()

    db_company.name = company.name
    db_company.registration_number = company.registration_number
    db_company.main_contact_number = company.main_contact_number
    db_company.secondary_contact_number = company.secondary_contact_number
    db_company.updated_at = datetime.datetime.now()

    db.commit()
    db.refresh(db_company)
    return db_company


def update_address(db: Session, company_id: int, address: schema.AddressUpdate):
    db_address: Address = db.query(models.Address).filter(models.Address.id == company_id).first()

    db_address.street_name = address.street_name
    db_address.street_number = address.street_number
    db_address.suburb = address.suburb
    db_address.city = address.city
    db_address.province_state = address.province_state
    db_address.postal_zip_code = address.postal_zip_code
    db_address.company_id = address.company_id
    db_address.updated_at = datetime.datetime.now()

    db.commit()
    db.refresh(db_address)
    return db_address
