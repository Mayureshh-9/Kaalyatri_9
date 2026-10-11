import random
import string
from fastapi import APIRouter, Depends, HTTPException, Form, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db

router = APIRouter(prefix="/api/payments", tags=["Payments"])

@router.post("/insert-update-payment")
async def insert_update_payment(
    id: Optional[int] = Form(None),
    booking_id: int = Form(...),
    amount: float = Form(...),
    status: Optional[str] = Form("Completed"),
    transaction_id: Optional[str] = Form(None),
    created_by: str = Form("system"),
    db: AsyncSession = Depends(get_db)
):
    try:
        tx_id = transaction_id or f"TXN-{"".join(random.choices(string.ascii_uppercase + string.digits, k=10))}"
        
        ins_res = await db.execute(text("""
            INSERT INTO admin.payments (booking_id, amount, status, transaction_id, created_date, updated_date)
            VALUES (:bid, :amount, :status, :tx_id, NOW(), NOW())
            RETURNING id
        """), {"bid": booking_id, "amount": amount, "status": status, "tx_id": tx_id})
        pay_id = ins_res.scalar()

        # Update booking status to CONFIRMED
        await db.execute(text("UPDATE admin.bookings SET status = 'CONFIRMED' WHERE id = :bid"), {"bid": booking_id})

        await db.commit()
        return {"status": 1, "message": "Payment processed successfully", "id": pay_id, "transaction_id": tx_id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getall-payments")
async def get_all_payments(
    p_booking_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_db)
):
    try:
        query_str = "SELECT * FROM admin.payments WHERE 1=1"
        params = {}
        if p_booking_id:
            query_str += " AND booking_id = :bid"
            params["bid"] = p_booking_id
        query_str += " ORDER BY id DESC"

        res = await db.execute(text(query_str), params)
        rows = res.fetchall()
        return {"status": 1, "data": [dict(r._mapping) for r in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
