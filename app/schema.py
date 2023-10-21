from datetime import datetime
from typing import Optional, Any, List

from pydantic import BaseModel, Json


class StatusBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class StatusCreate(StatusBase):
    pass


class UserBase(BaseModel):
    name: str
    username: str
    email: str


class UserCreate(UserBase):
    status_id: int
    password: str


class User(UserBase):
    id: int
    email_verified_at: Optional[datetime] = None
    remember_token: str


class Status(StatusBase):
    id: int
    users: list[User] = []

    class Config:
        from_attributes = True


class Ability(BaseModel):
    id: int
    name: str
    status: Status


class CompanyBase(BaseModel):
    name: str
    registration_number: str
    main_contact_number: str
    secondary_contact_number: Optional[str] = None

    class Config:
        orm_mode = True


class CompanyCreate(CompanyBase):
    user_id: int


class Company(CompanyBase):
    id: int
    user: User

    class Config:
        orm_mode = True


class ApplicationBase(BaseModel):
    name: str


class ApplicationCreate(ApplicationBase):
    company_id: int
    status_id: int


class Application(ApplicationBase):
    id: int
    company: CompanyBase
    status: StatusBase

    class Config:
        orm_mode = True


class Address(BaseModel):
    id: int
    street_name: str
    street_number: str
    suburb: str
    city: str
    province_state: str
    postal_zip_code: str
    country: str
    status: Status


class AccessTokenBase(BaseModel):
    token: str
    last_used_at: datetime


class AccessToken(AccessTokenBase):
    id: int
    status: Status
    application: Application

    class Config:
        orm_mode = True


class AccessTokenCreate(AccessTokenBase):
    token: str
    abilities: List[int]
    status_id: int
    application_id: int


class Dataset(BaseModel):
    id: int
    name: str
    description: str
    status: Status


class DatasetItem(BaseModel):
    id: int
    type: str
    file_path: str
    metadata: Json[Any]
