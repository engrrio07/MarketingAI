from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.content import Content
from app.services.analytics_service import get_content_analytics
from app.services.auth_service import get_current_user
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta

router = APIRouter()

class AnalyticsResponse(BaseModel):
    content_id: int
    views: int
    likes: int
    shares: int
    time_spent: float
    bounce_rate: float
    click_through_rate: float
    engagement_rate: float
    timestamp: datetime

@router.get("/content/{content_id}/analytics", response_model=List[AnalyticsResponse])
async def get_content_analytics_api(
    content_id: int, 
    start_date: datetime = None, 
    end_date: datetime = None, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=30)
    if not end_date:
        end_date = datetime.utcnow()
    
    analytics = get_content_analytics(db, content_id, start_date, end_date)
    return analytics