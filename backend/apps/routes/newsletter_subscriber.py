from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db

router = APIRouter(prefix="/api/newsletter", tags=["Newsletter Subscribers"])

@router.post("/insert-update-newsletter-subscriber")
async def insert_update_newsletter_subscriber(
    email: str = Form(...),
    created_by: str = Form("system"),
    db: AsyncSession = Depends(get_db)
):
    try:
        res = await db.execute(text("SELECT id FROM admin.newsletter_subscribers WHERE email = :email"), {"email": email})
        if res.first():
            return {"status": 1, "message": "You are already subscribed to Temporal Dispatches!"}

        ins_res = await db.execute(text("""
            INSERT INTO admin.newsletter_subscribers (email, created_date, updated_date)
            VALUES (:email, NOW(), NOW())
            RETURNING id
        """), {"email": email})
        sub_id = ins_res.scalar()
        await db.commit()
        return {"status": 1, "message": "Subscribed to Temporal Dispatches successfully!", "id": sub_id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
