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
    pass


class ApplicationBase(BaseModel):
    name: str


class ApplicationCreate(ApplicationBase):
    company_id: int
    status_id: int


class ApplicationUpdate(ApplicationBase):
    application_id: int
    company_id: int
    status_id: int


class Application(ApplicationBase):
    id: int
    company: CompanyBase
    status: StatusBase

    class Config:
        orm_mode = True


class Company(CompanyBase):
    id: int
    user: User
    applications: list[Application]

    class Config:
        orm_mode = True


class CompanyUpdate(CompanyBase):
    company_id: int

    class Config:
        orm_mode = True


class AddressBase(BaseModel):
    street_name: str
    street_number: str
    suburb: str
    city: str
    province_state: str
    postal_zip_code: str
    country: str


class Address(AddressBase):
    id: int
    company: Company


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    company_id: int


class AccessTokenBase(BaseModel):
    token: str
    expires_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None


class AccessToken(AccessTokenBase):
    id: int
    application: Application

    class Config:
        orm_mode = True


class AccessTokenCreate(AccessTokenBase):
    token: str
    abilities: List[int]
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
