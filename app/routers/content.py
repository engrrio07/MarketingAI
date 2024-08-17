from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.content import Content
from app.services.ai_service import generate_content
from pydantic import BaseModel
from typing import List

router = APIRouter()

class ContentRequest(BaseModel):
    prompt: str

class ContentResponse(BaseModel):
    id: int
    title: str
    body: str

@router.post("/generate", response_model=ContentResponse)
def create_content(content_request: ContentRequest, db: Session = Depends(get_db)):
    try:
        generated_content = generate_content(content_request.prompt)
        db_content = Content(title=generated_content["title"], body=generated_content["body"])
        db.add(db_content)
        db.commit()
        db.refresh(db_content)
        return db_content
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{content_id}", response_model=ContentResponse)
def read_content(content_id: int, db: Session = Depends(get_db)):
    content = db.query(Content).filter(Content.id == content_id).first()
    if content is None:
        raise HTTPException(status_code=404, detail="Content not found")
    return content

@router.get("/", response_model=List[ContentResponse])
def list_contents(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    contents = db.query(Content).offset(skip).limit(limit).all()
    return contents