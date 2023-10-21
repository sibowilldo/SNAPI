from sqlalchemy.orm import Session

from . import models, schema
from .schema import Application
from .utils.auth import get_hashed_password


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


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


def get_applications(db: Session, skip: int = 0, limit: int = -1):
    return db.query(models.Application).offset(skip).limit(limit).all()


def get_application_by_id(db: Session, application_id: int) -> Application:
    return db.query(models.Application).filter(models.Application.id == application_id).first()


def get_applications_by_company_id(db: Session, company_id: int, skip: int = 0, limit: int = -1):
    return db.query(models.Application).filter(models.Application.company_id == company_id).offset(skip).limit(
        limit).all()


def get_companies(db: Session, user_id: int, skip: int = 0, limit: int = -1):
    return db.query(models.Company).filter(models.Company.user_id == user_id).offset(skip).limit(limit).all()


def create_token(db: Session, access_token: schema.AccessTokenCreate):
    db_access_token = models.AccessToken(token=access_token.token, status_id=access_token.status_id,
                                        application_id=access_token.application_id)

    db_access_token.abilities.append()

    db.add(db_access_token)
    db.commit()
    db.refresh(db_access_token)
    return db_access_token
