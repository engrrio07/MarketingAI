import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.content import Content
from app.models.content_analytics import ContentAnalytics

def generate_random_analytics(content_id: int):
    return {
        "content_id": content_id,
        "views": random.randint(10, 1000),
        "likes": random.randint(5, 500),
        "shares": random.randint(1, 100),
        "time_spent": random.uniform(10, 300),
        "bounce_rate": random.uniform(0.1, 0.9),
        "click_through_rate": random.uniform(0.01, 0.2),
        "engagement_rate": random.uniform(0.05, 0.5),
        "timestamp": datetime.utcnow()
    }

def update_content_analytics(db: Session):
    contents = db.query(Content).all()
    for content in contents:
        analytics_data = generate_random_analytics(content.id)
        db_analytics = ContentAnalytics(**analytics_data)
        db.add(db_analytics)
    db.commit()

def get_content_analytics(db: Session, content_id: int, start_date: datetime, end_date: datetime):
    return db.query(ContentAnalytics).filter(
        ContentAnalytics.content_id == content_id,
        ContentAnalytics.timestamp >= start_date,
        ContentAnalytics.timestamp <= end_date
    ).all()