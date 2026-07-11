from sqlalchemy import Column, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
import uuid

from app.database import Base
from app.models.user import GUID


class Simulation(Base):
    __tablename__ = "simulations"

    id = Column(GUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(GUID, ForeignKey("users.id"), nullable=False)
    profile_id = Column(GUID, ForeignKey("profiles.id"), nullable=False)
    
    hypothesis = Column(JSON, default=dict)
    simulated_milestones = Column(JSON, default=list)
    risk_assessment = Column(JSON, default=dict)
    comparison = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
