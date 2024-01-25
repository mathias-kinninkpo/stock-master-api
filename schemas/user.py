from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    manager = "manager"
    # Ajoutez d'autres rôles au besoin

class UserBase(BaseModel):
    username: str
    password: str
    full_name: str
    email: str
    

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int
    role: str

    class Config:
        orm_mode = True
        from_attributes=True

