from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
import uuid

from app.database import Base
from app.models.user import GUID


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    
    birth_year = Column(Integer)
    gender = Column(String(10))
    education = Column(String(50))
    major = Column(String(100))
    school = Column(String(100))
    
    skills = Column(JSON, default=list)
    personality_type = Column(String(20))
    current_industry = Column(String(50))
    current_role = Column(String(100))
    work_years = Column(Integer)
    salary_range = Column(String(50))
    
    career_history = Column(JSON, default=list)
    resume_text = Column(Text)
    
    version = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
