from sqlalchemy import Column, Integer, Text
from .database import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    company = Column(Text, nullable=False)
