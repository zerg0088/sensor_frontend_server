from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    place_id : Optional[int] = -1
    phone: Optional[List[str]] = []

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None
    email: Optional[str] = None

class UserInDBBase(UserBase):
    id: int
    password: Optional[str] = None

    class Config:
        orm_mode = True

class UserRead(UserInDBBase):
    pass
