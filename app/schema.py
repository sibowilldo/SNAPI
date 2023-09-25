from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, Json


class UserBase(BaseModel):
    name: str
    is_active: bool
    username: str
    email: str
    email_verified_at: Optional[datetime] = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    hashed_password: str


class StatusBase(BaseModel):
    pass


class StatusCreate(StatusBase):
    pass


class Status(StatusBase):
    id: int
    users: list[User] = []

    class Config:
        from_attributes = True


class Application(BaseModel):
    id: int
    name: str
    user: User
    status: Status


class Ability(BaseModel):
    id: int
    name: str
    status: Status

class AccessToken(BaseModel):
    id: int
    token: str
    expires_at: datetime


class Company(BaseModel):
    id: int
    name: str
    registration_number: str
    main_contact_number: str
    secondary_contact_number: Optional[str] = None
    owner: User


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