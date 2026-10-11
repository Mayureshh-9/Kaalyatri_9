from fastapi import APIRouter, Depends, HTTPException, Form
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db

router = APIRouter(prefix="/api/contact", tags=["Contact Messages"])

@router.post("/insert-update-contact-message")
async def insert_update_contact_message(
    name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None),
    subject: Optional[str] = Form(None),
    message: str = Form(...),
    created_by: str = Form("system"),
    db: AsyncSession = Depends(get_db)
):
    try:
        ins_res = await db.execute(text("""
            INSERT INTO admin.contact_messages (name, email, phone, subject, message, is_read, created_date, updated_date)
            VALUES (:name, :email, :phone, :subject, :message, False, NOW(), NOW())
            RETURNING id
        """), {"name": name, "email": email, "phone": phone, "subject": subject, "message": message})
        msg_id = ins_res.scalar()
        await db.commit()
        return {"status": 1, "message": "Thank you! Your message has been beamed to our temporal advisors.", "id": msg_id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getall-messages")
async def get_all_contact_messages(db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(text("SELECT * FROM admin.contact_messages ORDER BY id DESC"))
        rows = res.fetchall()
        return {"status": 1, "data": [dict(r._mapping) for r in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
