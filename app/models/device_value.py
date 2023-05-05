from sqlalchemy import Boolean, Column, String, Text, Float, Integer, DateTime
from sqlalchemy.sql import text
from sqlalchemy.dialects.mysql import INTEGER
from app.db.session import Base


class DeviceValue(Base):
    __tablename__ = "device_value"

    id = Column(INTEGER(display_width=11, unsigned=True), primary_key=True, index=True)
    did = Column(Integer, index=True)
    v1 = Column(Integer, nullable =True)
    v2 = Column(Integer, nullable =True)
    v3 = Column(Integer, nullable =True)
    c1 = Column(Integer, nullable =True)
    c2 = Column(Integer, nullable =True)
    c3 = Column(Integer, nullable =True)
    e1 = Column(Integer, nullable =True, default=0)
    e2 = Column(Integer, nullable =True, default=0)
    e3 = Column(Integer, nullable =True, default=0)
    r1 = Column(Integer, nullable =True)
    r2 = Column(Integer, nullable =True)
    r3 = Column(Integer, nullable =True)
    r4 = Column(Integer, nullable =True)
    r5 = Column(Integer, nullable =True)
    timestamp = Column(DateTime(), server_default=text('NOW()'))
    
    

# CREATE TABLE device_value (
#   id INT(11) NOT NULL AUTO_INCREMENT,
#   did INT(11) NOT NULL,
#   v1 INT(11),
#   v2 INT(11),
#   v3 INT(11),
#   c1 INT(11),
#   c2 INT(11),
#   c3 INT(11),
#   e1 INT(11),
#   e2 INT(11),
#   e3 INT(11),
#   r1 INT(11),
#   r2 INT(11),
#   r3 INT(11),
#   r4 INT(11),
#   r5 INT(11),
#   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
#   PRIMARY KEY (id)
# );
