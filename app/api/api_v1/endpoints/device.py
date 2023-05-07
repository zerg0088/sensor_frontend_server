import os
from twilio.rest import Client

from typing import Any

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from app.models.device import Device
from app.schemas.device import DeviceRead, DeviceUpdate, DeviceCreate
from app.schemas.device_value import DeviceValueRead, DeviceValueUpdate, DeviceValueCreate
from app.api.depends import get_db
from sqlalchemy.orm import Session
from app.crud.device import crud_device
from app.crud.user import crud_user
from app.crud.device_value import crud_device_value
from fastapi.encoders import jsonable_encoder

account_sid = "AC0ea6d0032411623d41ad71b0bd680917"
auth_token = "4f38c2627ce208f158655ec732134aac"
client = Client(account_sid, auth_token)

router = APIRouter()

@router.get("/device_list", response_model=list[DeviceRead])
def read_devices(db: Session = Depends(get_db)) -> list[DeviceRead]:
    devices = crud_device.get_all(db)
    json_compatible_item_data = jsonable_encoder(devices)
    print(json_compatible_item_data)
    return devices

# http://127.0.0.1:8000/api/v1/device_list/{}
@router.get("/device_list/{place_id}", response_model=list[DeviceRead])
def read_devices_by_place_id(place_id: int, db: Session = Depends(get_db)) -> list[DeviceRead]:
    if place_id == 0 : 
        devices = crud_device.get_all(db)    
    else :
        devices = crud_device.get_by_place_id(db, place_id)
    print(devices)
    return devices

@router.post("/add_device")
def add_device(device: DeviceCreate, db: Session = Depends(get_db)):
    return crud_device.create(db=db, obj_in=device)


# http://127.0.0.1:8000/api/v1/value_list
@router.get("/value_list", response_model=list[DeviceValueRead])
def read_device_value_list(db: Session = Depends(get_db)) -> list[DeviceValueRead]:
    device_values = crud_device_value.get_all(db)
    json_compatible_item_data = jsonable_encoder(device_values)
    print(json_compatible_item_data)
    return device_values

# http://127.0.0.1:8000/api/v1/update_data/did
@router.get("/update_data/{did}")
def update_data(did: int, db: Session = Depends(get_db)) :
    device_value = crud_device_value.get_by_id(db, did)
    print(device_value)
    return device_value    

# http://127.0.0.1:8000/api/v1/chart/did
@router.get("/chart/{did}", response_model=list[DeviceValueRead])
def chart(did: int, db: Session = Depends(get_db)) -> list[DeviceValueRead]:
    device_values = crud_device_value.get_chart_by_id(db, did)
    print(device_values)
    return device_values
    
# 기준 전류 셋팅. 
@router.patch("/device_update/{device_id}", response_model=DeviceRead)
def update_device(*, device_id: int, device_in: DeviceUpdate, db: Session = Depends(get_db)) -> Any:
    device = crud_device.get(db, id=device_id)
    if not device:
        raise HTTPException(
            status_code=404,
            detail="device empty",
        )
    device = crud_device.update(db, db_obj=device, obj_in=device_in)
    return device   
    
    
# http://127.0.0.1:8000/api/v1/insert?did=1&v1=10&v2=20
@router.get("/insert")
def insert_data(did: int, v1 : int = None, v2 : int = None, v3 : int = None,
                c1 : int = None, c2 : int = None, c3 : int = None,
                e1 : int = 0, e2 : int = 0, e3 : int = 0,
                r1 : int = None, r2 : int = None, r3 : int = None, r4 : int = None, r5 : int = None,
                db: Session = Depends(get_db)):
    device_value = DeviceValueCreate(
        did=did,
        v1=v1, v2=v2, v3=v3,
        c1=c1, c2=c2, c3=c3,
        e1=e1, e2=e2, e3=e3,
        r1=r1, r2=r2, r3=r3, r4=r4, r5=r5
    )
    
    device = crud_device.get_by_did(db, did)
    if device == None : 
        return 'device 없음'
        
    users = crud_user.get_by_place(db, place_id=device.place_id)
    
    phoneList = []
    if users != None :
        for user in users :
            if len(user.phone) > 5 :
                phoneList.append(user.phone)
        
    if(e1 > 0) : 
        if(device.latest_ch1_error == 0) :
            device.latest_ch1_error = 1
            update_data = DeviceUpdate(latest_ch1_error=1)
            crud_device.update(db, db_obj=device, obj_in=update_data)
            sendSms(device.name,1,phoneList)
            print("sms fire 1")
    else : 
        if(device.latest_ch1_error == 1) :
            device.latest_ch1_error = 0
            update_data = DeviceUpdate(latest_ch1_error=0)
            crud_device.update(db, db_obj=device, obj_in=update_data)
            print("to zero 1")
            
    if(e2 > 0) : 
        if(device.latest_ch2_error == 0) :
            device.latest_ch2_error = 1
            update_data = DeviceUpdate(latest_ch2_error=1)
            crud_device.update(db, db_obj=device, obj_in=update_data)
            sendSms(device.name,2,phoneList)
            print("sms fire 2")
    else : 
        if(device.latest_ch2_error == 1) :
            device.latest_ch2_error = 0
            update_data = DeviceUpdate(latest_ch2_error=0)
            crud_device.update(db, db_obj=device, obj_in=update_data)
            print("to zero 2")      
            
    if(e3 > 0) : 
        if(device.latest_ch3_error == 0) :
            device.latest_ch3_error = 1
            update_data = DeviceUpdate(latest_ch3_error=1)
            crud_device.update(db, db_obj=device, obj_in=update_data)
            sendSms(device.name,3,phoneList)
            print("sms fire 3")
    else : 
        if(device.latest_ch3_error == 1) :
            device.latest_ch3_error = 0
            update_data = DeviceUpdate(latest_ch3_error=0)
            crud_device.update(db, db_obj=device, obj_in=update_data)
            print("to zero 3")                

    return crud_device_value.create(db=db, obj_in=device_value)

def sendSms(name, ch, list) :
    for number in list : 
        temp = "+82" + number[1:]  
        message = client.messages.create(
            body= name + '디바이스 CH' + str(ch) + '에 문제가 생겼습니다.',
            from_='+12705618731',
            to=temp
        )    
