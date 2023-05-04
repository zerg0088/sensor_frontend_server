from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.device_value import DeviceValue
from app.schemas.device_value import DeviceValueCreate, DeviceValueUpdate
from sqlalchemy import Column, Integer, String, Boolean


class CRUDDeviceValue(CRUDBase[DeviceValue, DeviceValueCreate, DeviceValueUpdate]):
    def get_all2(self, db: Session) -> list[DeviceValue]:
        return db.query(DeviceValue).all()
    # def get_by_id(self, db: Session, *, id: Integer) -> Optional[Device]:
    #     return db.query(Device).filter(Device.id == id).first()
    
    # def get_all_device(self, db: Session, *, obj_in: DeviceCreate) :
        
    # def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
    #     return db.query(User).filter(User.email == email).first()

    # def create_superuser(self, db: Session, *, obj_in: UserCreate) -> User:
    #     db_obj = User(
    #         email=obj_in.email,
    #         password=get_password_hash(obj_in.password),
    #         is_superuser=obj_in.is_superuser
    #     )
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     return db_obj

    # def create(self, db: Session, *, obj_in: UserCreate) -> User:
    #     db_obj = User(
    #         email=obj_in.email,
    #         password=get_password_hash(obj_in.password),
    #         organization = obj_in.organization,
    #     )
    #     db.add(db_obj)
    #     db.commit()
    #     db.refresh(db_obj)
    #     del db_obj.password
    #     return db_obj

    # def update(self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]) -> User:
    #     if isinstance(obj_in, dict):
    #         update_data = obj_in
    #     else:
    #         update_data = obj_in.dict(exclude_unset=True)
    #     if "password" in update_data:
    #         hashed_password = get_password_hash(update_data["password"])
    #         update_data["password"] = hashed_password
    #     return super().update(db, db_obj=db_obj, obj_in=update_data)

    # def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
    #     user = self.get_by_email(db, email=email)
    #     if not user:
    #         return None
    #     if not verify_password(password, user.password):
    #         return None
    #     return user

    # def is_active(self, user: User) -> bool:
    #     return user.is_active

    # def is_superuser(self, user: User) -> bool:
    #     return user.is_superuser

crud_device_value = CRUDDeviceValue(DeviceValue)
