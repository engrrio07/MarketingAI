from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class ContentAnalytics(Base):
    __tablename__ = "content_analytics"

    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer, ForeignKey("contents.id"))
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    time_spent = Column(Float, default=0.0)  # Average time spent in seconds
    bounce_rate = Column(Float, default=0.0)
    click_through_rate = Column(Float, default=0.0)
    engagement_rate = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)

    content = relationship("Content", back_populates="analytics")