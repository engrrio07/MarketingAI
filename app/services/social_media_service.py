from app.models.social_media_post import SocialMediaPost
from sqlalchemy.orm import Session
from datetime import datetime

def create_social_media_post(db: Session, content: str, scheduled_time: datetime, platform: str) -> SocialMediaPost:
    post = SocialMediaPost(content=content, scheduled_time=scheduled_time, platform=platform)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post