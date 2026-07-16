from sqlalchemy import Column, String, JSON, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
import uuid

from app.database import Base
from app.models.user import GUID


class Plan(Base):
    __tablename__ = "plans"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    diagnosis_id = Column(GUID, ForeignKey("diagnoses.id", ondelete="CASCADE"), nullable=False)
    
    plan_type = Column(String(20), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    milestones = Column(JSON, default=list)
    recommended_path = Column(JSON, default=dict)
    alternative_paths = Column(JSON, default=list)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())