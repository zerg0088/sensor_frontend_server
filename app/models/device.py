from sqlalchemy import Boolean, Column, String, Text, Float, Integer, DateTime
from sqlalchemy.sql import text
from sqlalchemy.dialects.mysql import INTEGER
from app.db.session import Base


class Device(Base):
    __tablename__ = "device"

    id = Column(INTEGER(display_width=11, unsigned=True), primary_key=True, autoincrement=True, index=True)
    name = Column(String(255))
    status = Column(String(10))
    alert_v_rate1 = Column(Float)
    alert_v_rate2 = Column(Float)
    alert_v_rate3 = Column(Float)
    alert_a_rate1 = Column(Float)
    alert_a_rate2 = Column(Float)
    alert_a_rate3 = Column(Float)
    place_id = Column(Integer, nullable=False)
    floor = Column(Integer)
    number = Column(String(10))
    create_at = Column(DateTime(), server_default=text('NOW()'))
    
