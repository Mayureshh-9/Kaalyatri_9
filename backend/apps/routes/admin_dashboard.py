from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db
from logger import logger

router = APIRouter(prefix="/api/admin", tags=["Admin Dashboard"])

@router.get("/stats")
async def get_admin_stats(db: AsyncSession = Depends(get_db)):
    try:
        dest_count = (await db.execute(text("SELECT COUNT(*) FROM admin.destinations"))).scalar() or 0
        booking_count = (await db.execute(text("SELECT COUNT(*) FROM admin.bookings"))).scalar() or 0
        user_count = (await db.execute(text("SELECT COUNT(*) FROM admin.users"))).scalar() or 0
        revenue = (await db.execute(text("SELECT COALESCE(SUM(amount), 0) FROM admin.payments WHERE status = 'Completed' OR status = 'SUCCESS'"))).scalar() or 0
        subscriber_count = (await db.execute(text("SELECT COUNT(*) FROM admin.newsletter_subscribers"))).scalar() or 0
        unread_messages = (await db.execute(text("SELECT COUNT(*) FROM admin.contact_messages WHERE is_read = False"))).scalar() or 0

        return {
            "status": 1,
            "data": {
                "destinations": dest_count,
                "bookings": booking_count,
                "users": user_count,
                "revenue_inr": float(revenue),
                "subscribers": subscriber_count,
                "unread_messages": unread_messages
            }
        }
    except Exception as e:
        logger.exception("Error getting admin stats")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all-bookings")
async def get_all_bookings_admin(db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(text("""
            SELECT b.*, d.name as destination_name, d.era, d.year_label, d.image_emoji
            FROM admin.bookings b
            LEFT JOIN admin.destinations d ON b.destination_id = d.id
            ORDER BY b.id DESC
        """))
        rows = res.fetchall()
        return {"status": 1, "data": [dict(r._mapping) for r in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
