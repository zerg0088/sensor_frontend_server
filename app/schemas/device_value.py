from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DeviceBase(BaseModel): 
    did: Optional[int] = 0
    v1: Optional[int] = 0
    v2: Optional[int] = 0
    v3: Optional[int] = 0
    c1: Optional[int] = 0
    c2: Optional[int] = 0
    c3: Optional[int] = 0
    e1: Optional[int] = 0
    e2: Optional[int] = 0
    e3: Optional[int] = 0
    r1: Optional[int] = 0
    r2: Optional[int] = 0
    r3: Optional[int] = 0
    r4: Optional[int] = 0
    r5: Optional[int] = 0
    timestamp: Optional[datetime] = None


class DeviceValueCreate(DeviceBase):
    pass


class DeviceValueUpdate(DeviceBase):
    pass
    # password: Optional[str] = None


class DeviceValueInDBBase(DeviceBase):
    # id: int
    # password: Optional[str] = None

    class Config:
        orm_mode = True


class DeviceValueRead(DeviceValueInDBBase):
    pass
