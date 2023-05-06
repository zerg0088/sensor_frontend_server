from sqlalchemy import Boolean, Column, String, Text, Float, Integer, DateTime
from sqlalchemy.sql import text
from sqlalchemy.dialects.mysql import INTEGER
from app.db.session import Base


class Place(Base):
    __tablename__ = "place"

    id = Column(INTEGER(display_width=11, unsigned=True), primary_key=True, autoincrement=True, index=True)
    name = Column(String(255))
