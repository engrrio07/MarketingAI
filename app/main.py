from fastapi import FastAPI, BackgroundTasks
from app.database import engine, Base, SessionLocal
from app.routers import content, auth, social_media, analytics
from app.services.analytics_service import update_content_analytics
import asyncio

# # Drop all tables
# from app.models import user, social_media_post
# Base.metadata.drop_all(bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(content.router, prefix="/api/content", tags=["content"])
app.include_router(social_media.router, prefix="/api/social-media", tags=["social-media"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])

async def update_analytics_periodically():
    while True:
        db = SessionLocal()
        try:
            update_content_analytics(db)
        finally:
            db.close()
        await asyncio.sleep(3600)  # Update every hour

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(update_analytics_periodically())

@app.get("/")
async def root():
    return {"message": "Welcome to MarketingAI"}