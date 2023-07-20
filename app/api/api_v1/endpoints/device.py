import os
#from twilio.rest import Client

from typing import Any

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from app.models.device import Device
from app.schemas.device import DeviceRead, DeviceUpdate, DeviceCreate, DeviceRemove
from app.schemas.device_value import DeviceValueRead, DeviceValueUpdate, DeviceValueCreate
from app.api.depends import get_db
from sqlalchemy.orm import Session
from app.crud.device import crud_device
from app.crud.user import crud_user
from app.crud.place import crud_place
from app.crud.device_value import crud_device_value
from fastapi.encoders import jsonable_encoder
#from app.core.config import settings
import csv
from io import StringIO
from fastapi.responses import StreamingResponse
import base64
import requests
import re


#client = Client(settings.SMS_SID, settings.SMS_AUTH_TOKEN)
router = APIRouter()

@router.get("/device_list", response_model=list[DeviceRead])
def read_devices(db: Session = Depends(get_db)) -> list[DeviceRead]:
    devices = crud_device.get_all(db)
    # json_compatible_item_data = jsonable_encoder(devices)
    # print(json_compatible_item_data)
    return devices

# http://127.0.0.1:8000/api/v1/device_list/{}
@router.get("/device_list/{place_id}", response_model=list[DeviceRead])
def read_devices_by_place_id(place_id: int, db: Session = Depends(get_db)) -> list[DeviceRead]:
    if place_id == 0 : 
        devices = crud_device.get_all(db)    
    else :
        devices = crud_device.get_by_place_id(db, place_id)
    # print(devices)
    return devices

@router.delete("/remove_device/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    print(device_id)
    device = crud_device.get(db=db, id=device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    
    crud_device_value.remove_by_did(db, did=device_id) 
    crud_device.remove(db=db, id=device_id)
    return {"message": "Device deleted"}

@router.post("/add_device")
def add_device(device: DeviceCreate, db: Session = Depends(get_db)):
    return crud_device.create(db=db, obj_in=device)

# http://127.0.0.1:8000/api/v1/value_list
@router.get("/value_list", response_model=list[DeviceValueRead])
def read_device_value_list(db: Session = Depends(get_db)) -> list[DeviceValueRead]:
    device_values = crud_device_value.get_all(db)
    # json_compatible_item_data = jsonable_encoder(device_values)
    # print(json_compatible_item_data)
    return device_values

# http://127.0.0.1:8000/api/v1/update_data/did
@router.get("/update_data/{did}")
def update_data(did: int, db: Session = Depends(get_db)) :
    device_value = crud_device_value.get_by_id(db, did)
    # print(device_value)
    return device_value    

# http://127.0.0.1:8000/api/v1/chart/did
@router.get("/chart/{did}", response_model=list[DeviceValueRead])
def chart(did: int, db: Session = Depends(get_db)) -> list[DeviceValueRead]:
    device_values = crud_device_value.get_chart_by_id(db, did)
    # print(device_values)
    return device_values

# http://127.0.0.1:8000/api/v1/download/did
@router.get("/download/{did}", response_model=list[DeviceValueRead])
def download(did: int, db: Session = Depends(get_db)):
    device_values = crud_device_value.get_datas_by_id(db, did)

    csv_data = StringIO()
    writer = csv.writer(csv_data)
    writer.writerows(device_values)

    response = StreamingResponse(
        iter([csv_data.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=data.csv"
        }
    )

    return response
    
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
    
    place = crud_place.get_by_id(db, device.place_id).name
    users = crud_user.get_by_place(db, place_id=device.place_id) # phones
    admins = crud_user.get_superuser(db) # phone 
    phoneSet = set()
    if users != None :
        for user in users :
            for phone in user.phone :
                if len(phone) > 5 :
                    phoneSet.add(phone)
                
    if admins != None :
        for user in admins :
            for phone in user.phone :
                if len(phone) > 5 :
                    phoneSet.add(phone)
    if(e1 > 0) : 
        if(device.latest_ch1_error == 0) :
            device.latest_ch1_error = 1
            update_data = DeviceUpdate(latest_ch1_error=1)
            crud_device.update(db, db_obj=device, obj_in=update_data)
            sendSms(place, device.name,1,list(phoneSet))
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
            sendSms(place, device.name,2,list(phoneSet))
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
            sendSms(place, device.name,3,list(phoneSet))
            print("sms fire 3")
    else : 
        if(device.latest_ch3_error == 1) :
            device.latest_ch3_error = 0
            update_data = DeviceUpdate(latest_ch3_error=0)
            crud_device.update(db, db_obj=device, obj_in=update_data)
            print("to zero 3")                

    return crud_device_value.create(db=db, obj_in=device_value)

def sendSms(position, name, ch, list) :
    for number in list : 
        message = position + ' ' + name + '고전압기 CH.' + str(ch) + '에 문제가 발생하였습니다.'
        send_message(message, format_phone_number(number))
        # message = client.messages.create(
        #     body= position + ' ' + name + '고전압기 CH.' + str(ch) + '에 문제가 발생하였습니다.',
        #     from_='+12705618731',
        #     to=temp
        # )    
        
def send_message(msg, rphone):
    sms_url = 'https://sslsms.cafe24.com/sms_sender.php'

    user_id = base64.b64encode("alink2016".encode('utf-8'))
    secure = base64.b64encode("7fa0085fa5cb29565a1d27fe0d93c594".encode('utf-8')) 
    mode = base64.b64encode('1'.encode('utf-8'))
    SMS_SENDER_NUMBER = ["051", "972", "3693"]
    
    sphone1 = base64.b64encode(SMS_SENDER_NUMBER[0].encode('utf-8'))
    sphone2 = base64.b64encode(SMS_SENDER_NUMBER[1].encode('utf-8'))
    sphone3 = base64.b64encode(SMS_SENDER_NUMBER[2].encode('utf-8'))

    rphone = base64.b64encode(rphone.encode('utf-8'))
    msg = base64.b64encode(msg.encode('utf-8'))
    testflag = base64.b64encode('N'.encode('utf-8'))
    data = {
      'user_id': user_id,
      'secure': secure,
      'mode': mode,
      'sphone1': sphone1,
      'sphone2': sphone2,
      'sphone3': sphone3,
      'rphone': rphone,
      'msg': msg,
      'testflag' : testflag
    }
    decoded_data = {
      'user_id' : base64.b64decode(user_id).decode('utf-8'),
      'secure': base64.b64decode(secure).decode('utf-8'),
      'mode': base64.b64decode(mode).decode('utf-8'),
      'sphone1': base64.b64decode(sphone1).decode('utf-8'),
      'sphone2': base64.b64decode(sphone2).decode('utf-8'),
      'sphone3': base64.b64decode(sphone3).decode('utf-8'),
      'rphone': base64.b64decode(rphone).decode('utf-8'),
      'msg': base64.b64decode(msg).decode('utf-8'),
      'testflag' : base64.b64decode(testflag).decode('utf-8')
    }
    print(decoded_data) 

    res = requests.post(sms_url, data)
    print(res)
    return res.status_code

def format_phone_number(text):
    # 숫자만 추출하여 하이픈(-)을 제외한 숫자들을 합침
    numbers = "".join(re.findall(r'\d', text))

    # 핸드폰 번호 형식에 맞게 변환
    if len(numbers) == 10:
        formatted_number = re.sub(r'(\d{3})(\d{3})(\d{4})', r'\1-\2-\3', numbers)
    elif len(numbers) == 11:
        formatted_number = re.sub(r'(\d{3})(\d{4})(\d{4})', r'\1-\2-\3', numbers)
    else:
        # 유효한 핸드폰 번호가 아닐 경우, 원본 텍스트 반환
        formatted_number = text

    return formatted_number
