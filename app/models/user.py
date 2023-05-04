from sqlalchemy import Boolean, Column, String, Text
from sqlalchemy.dialects.mysql import INTEGER
from app.db.session import Base


class User(Base):
    __tablename__ = "user"

    id = Column(INTEGER(display_width=11, unsigned=True), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    organization = Column(String(255), default="")
    devices = Column(Text, default="")
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean(), default=False)
    