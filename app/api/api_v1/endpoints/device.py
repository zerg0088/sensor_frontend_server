from typing import Any

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from app.models.device import Device
from app.schemas.device import DeviceRead, DeviceUpdate, DeviceCreate
from app.schemas.device_value import DeviceValueRead, DeviceValueUpdate, DeviceValueCreate
from app.api.depends import get_db
from sqlalchemy.orm import Session
from app.crud.device import crud_device
from app.crud.device_value import crud_device_value
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("/device_list", response_model=list[DeviceRead])
def read_devices(db: Session = Depends(get_db)) -> list[DeviceRead]:
    devices = crud_device.get_all(db)
    json_compatible_item_data = jsonable_encoder(devices)
    print(json_compatible_item_data)
    return devices


@router.post("/add_device")
def add_device(device: DeviceCreate,  db: Session = Depends(get_db)):
    return crud_device.create(db=db, obj_in=device)


# http://127.0.0.1:8000/api/v1/value_list
@router.get("/value_list", response_model=list[DeviceValueRead])
def read_device_value_list(db: Session = Depends(get_db)) -> list[DeviceValueRead]:
    device_values = crud_device_value.get_all(db)
    json_compatible_item_data = jsonable_encoder(device_values)
    print(json_compatible_item_data)
    return device_values


# http://127.0.0.1:8000/api/v1/insert?did=1&v1=10&v2=20
@router.get("/insert")
def insert_data(did: int, v1 : int = None, v2 : int = None, v3 : int = None,
                c1 : int = None, c2 : int = None, c3 : int = None,
                e1 : int = None, e2 : int = None, e3 : int = None,
                r1 : int = None, r2 : int = None, r3 : int = None, r4 : int = None, r5 : int = None,
                db: Session = Depends(get_db)):
    device_value = DeviceValueCreate(
        did=did,
        v1=v1, v2=v2, v3=v3,
        c1=c1, c2=c2, c3=c3,
        e1=e1, e2=e2, e3=e3,
        r1=r1, r2=r2, r3=r3, r4=r4, r5=r5
    )
    return crud_device_value.create(db=db, obj_in=device_value)

