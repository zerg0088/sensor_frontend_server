from sqlalchemy import Boolean, Column, String, Text, Integer, ARRAY
from sqlalchemy.dialects.mysql import INTEGER, JSON
from app.db.session import Base

class User(Base):
    __tablename__ = "user"

    id = Column(INTEGER(display_width=11, unsigned=True), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    phone = Column(JSON, default=[])
    place_id = Column(Integer, default=-1)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean(), default=False)
    