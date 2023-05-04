from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import urllib

from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import Base, engine, get_db
from app.schemas.device import DeviceCreate
from app.crud.device import crud_device

router = APIRouter()

def my_url_for(request: Request, name: str, **path_params: any) -> str:
    url = request.url_for(name, **path_params)
    parsed = list(urllib.parse.urlparse(url))
    parsed[1] = '43.201.115.217' 
    # parsed[1] = '127.0.0.1:8000'
    return urllib.parse.urlunparse(parsed)

templates = Jinja2Templates(directory="app/templates") 
templates.env.globals['my_url_for'] = my_url_for

@router.get("/login", response_class=HTMLResponse) 
async def login(request: Request): 
    return templates.TemplateResponse("login.html", {"request": request}) 

@router.get("/main", response_class=HTMLResponse) 
async def main(request: Request, db: Session = Depends(get_db)): 
    devices = crud_device.get_all(db)
    return templates.TemplateResponse("main.html", {"request": request, "devices": devices, "user": 0}) 

    