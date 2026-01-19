from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from app.database.connection import Base
import uuid
from datetime import datetime

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, unique=True, nullable=False)
    client_secret = Column(String, nullable=False)