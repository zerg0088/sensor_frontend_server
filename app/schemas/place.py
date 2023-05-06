from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class PlaceBase(BaseModel): 
    name: Optional[str] = ""


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(PlaceBase):
    pass
    # password: Optional[str] = None


class PlaceInDBBase(PlaceBase):
    id: int
    # password: Optional[str] = None

    class Config:
        orm_mode = True


class PlaceRead(PlaceInDBBase):
    pass
