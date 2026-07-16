from sqlalchemy import Column, Integer, Float, JSON, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
import uuid

from app.database import Base
from app.models.user import GUID


class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    profile_id = Column(GUID, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    profile_version = Column(Integer, nullable=False)
    
    health_score = Column(Float)
    dimensions = Column(JSON, default=dict)
    strengths = Column(JSON, default=list)
    risks = Column(JSON, default=list)
    summary = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())