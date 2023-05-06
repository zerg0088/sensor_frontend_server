from typing import Any

from fastapi import APIRouter, Depends, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from app.models.place import Place
from app.schemas.place import PlaceRead, PlaceUpdate, PlaceCreate

from app.api.depends import get_db
from sqlalchemy.orm import Session
from app.crud.place import crud_place
from fastapi.encoders import jsonable_encoder

router = APIRouter()

## http://127.0.0.1:8000/api/v1/place_list
@router.get("/place_list", response_model=list[PlaceRead])
def read_devices(db: Session = Depends(get_db)) -> list[PlaceRead]:
    devices = crud_place.get_all(db)
    return devices

## http://127.0.0.1:8000/api/v1/add_place
@router.post("/add_place")
def add_place(place: PlaceCreate,  db: Session = Depends(get_db)):
    return crud_place.create(db=db, obj_in=place)

