from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.social_media_post import SocialMediaPost
from app.services.auth_service import get_current_user
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class SocialMediaPostCreate(BaseModel):
    content: str
    platform: str
    scheduled_time: datetime

@router.post("/posts")
async def create_social_media_post(post: SocialMediaPostCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_post = SocialMediaPost(**post.dict(), user_id=current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/posts")
async def get_social_media_posts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(SocialMediaPost).filter(SocialMediaPost.user_id == current_user.id).all()

@router.delete("/posts")
async def delete_all_posts(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    try:
        db.query(SocialMediaPost).filter(SocialMediaPost.user_id == current_user.id).delete()
        db.commit()
        return {"message": "All posts deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred while deleting posts: {str(e)}")