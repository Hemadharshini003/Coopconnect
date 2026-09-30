import uuid
from sqlalchemy import Column, String
from app.db.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class District(Base):
    __tablename__ = "districts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False, default="Maharashtra")
    country = Column(String(100), nullable=False, default="India")
    code = Column(String(20), unique=True, nullable=False)
