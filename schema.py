from pydantic import BaseModel


class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    
class StatusBase(BaseModel):
    pass


class StatusCreate(StatusBase):
    pass


class Status(StatusBase):
    id: int
    users: list[User] = []

    class Config:
        orm_mode = True


