from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class DeviceBase(BaseModel): 
    id : Optional[int] = 0
    name: Optional[str] = ""
    status: Optional[str] = ""
    alert_v_rate1: Optional[float] = 0.0
    alert_v_rate2: Optional[float] = 0.0
    alert_v_rate3: Optional[float] = 0.0
    alert_a_rate1: Optional[float] = 0.0
    alert_a_rate2: Optional[float] = 0.0
    alert_a_rate3: Optional[float] = 0.0
    latest_ch1_error : Optional[bool] = False
    latest_ch2_error : Optional[bool] = False
    latest_ch3_error : Optional[bool] = False
    place_id : int = 0
    floor: Optional[int] = 0
    number: Optional[str] = ""
    create_at: Optional[datetime] = None


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass
    # password: Optional[str] = None


class DeviceInDBBase(DeviceBase):
    # id: int
    # password: Optional[str] = None

    class Config:
        orm_mode = True


class DeviceRead(DeviceInDBBase):
    pass
