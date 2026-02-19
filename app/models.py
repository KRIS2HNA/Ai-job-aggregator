from sqlalchemy import Column, Integer, Text, DateTime, String, ForeignKey
from sqlalchemy.sql import func
from .database import Base
from sqlalchemy.orm import relationship


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    company = Column(Text, nullable=False)
    location = Column(String(255))
    description  = Column(Text)
    apply_link = Column(String(500), unique=True)
    source = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True)
    
    name = Column(String(100), unique=True, nullable=False)
    
class JobSkill(Base):
    __tablename__ = "job_skills"
    
    job_id = Column(Integer, ForeignKey("jobs.id"), primary_key= True)
    skills_id = Column(Integer, ForeignKey("skills.id"), primary_key= True)
        
