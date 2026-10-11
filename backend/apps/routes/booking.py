import random
import string
import datetime
from datetime import date
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db
from logger import logger

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

def generate_pass_code(year_label: str = "2026") -> str:
    cleaned_year = year_label.replace(" ", "").replace("BCE", "-BCE").replace("CE", "-CE")
    rand_str = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"KY-{cleaned_year}-{rand_str}"

@router.post("/insert-update-booking")
async def insert_update_booking(
    id: Optional[int] = Form(None),
    destination_id: int = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    travelers: Optional[int] = Form(1),
    travel_date: str = Form(...),
    notes: Optional[str] = Form(None),
    status: Optional[str] = Form("CONFIRMED"),
    created_by: str = Form("system"),
    db: AsyncSession = Depends(get_db)
):
    try:
        try:
            parsed_date = date.fromisoformat(travel_date)
        except ValueError:
            parsed_date = date.today()

        booking_id = id

        # Try stored procedure first
        try:
            sp_query = text("""
                SELECT * FROM admin.insert_update_booking(
                    :p_destination_id, :p_full_name, :p_email, :p_phone,
                    :p_travelers, :p_travel_date, :p_notes, :p_status,
                    :p_created_by, :p_id
                )
            """)
            sp_res = await db.execute(sp_query, {
                "p_destination_id": destination_id,
                "p_full_name": full_name,
                "p_email": email,
                "p_phone": phone,
                "p_travelers": travelers,
                "p_travel_date": parsed_date,
                "p_notes": notes,
                "p_status": status,
                "p_created_by": created_by,
                "p_id": id
            })
            row = sp_res.first()
            if row:
                booking_id = row[0]
        except Exception:
            booking_id = None

        if not booking_id:
            # Fallback to direct SQL query
            if id:
                await db.execute(text("""
                    UPDATE admin.bookings SET
                        destination_id=:dest_id, full_name=:name, email=:email, phone=:phone,
                        travelers=:travelers, travel_date=:tdate, notes=:notes, status=:status, updated_date=NOW()
                    WHERE id=:id
                """), {
                    "id": id, "dest_id": destination_id, "name": full_name, "email": email,
                    "phone": phone, "travelers": travelers, "tdate": parsed_date, "notes": notes, "status": status
                })
                booking_id = id
            else:
                ins_res = await db.execute(text("""
                    INSERT INTO admin.bookings (
                        destination_id, full_name, email, phone, travelers, travel_date, notes, status, created_date, updated_date
                    ) VALUES (
                        :dest_id, :name, :email, :phone, :travelers, :tdate, :notes, :status, NOW(), NOW()
                    ) RETURNING id
                """), {
                    "dest_id": destination_id, "name": full_name, "email": email,
                    "phone": phone, "travelers": travelers, "tdate": parsed_date, "notes": notes, "status": status
                })
                booking_id = ins_res.scalar()

        # Fetch destination details for pass generation
        dest_res = await db.execute(text("SELECT name, year_label, era, image_emoji FROM admin.destinations WHERE id = :id"), {"id": destination_id})
        dest = dest_res.first()
        year_lbl = dest.year_label if dest else "2026"

        # Generate or fetch Temporal Pass ticket
        pass_res = await db.execute(text("SELECT * FROM admin.temporal_passes WHERE booking_id = :bid"), {"bid": booking_id})
        pass_row = pass_res.first()

        pass_code = None
        if pass_row:
            pass_code = pass_row._mapping["pass_code"]
        else:
            pass_code = generate_pass_code(year_lbl)
            qr_hash = f"HASH-{booking_id}-{pass_code}"
            await db.execute(text("""
                INSERT INTO admin.temporal_passes (booking_id, pass_code, qr_hash, status, issued_at, created_date, updated_date)
                VALUES (:bid, :pcode, :qhash, 'ACTIVE', NOW(), NOW(), NOW())
            """), {"bid": booking_id, "pcode": pass_code, "qhash": qr_hash})

        await db.commit()

        return {
            "status": 1,
            "message": "Booking confirmed successfully",
            "id": booking_id,
            "pass_code": pass_code
        }
    except Exception as e:
        await db.rollback()
        logger.exception("Error in insert_update_booking")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getall-bookings")
async def get_all_bookings(
    p_limit: int = Query(50, ge=1),
    p_offset: int = Query(0, ge=0),
    p_search: Optional[str] = None,
    p_status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        query_str = """
            SELECT b.*, d.name as destination_name, d.year_label, d.era, d.image_emoji
            FROM admin.bookings b
            LEFT JOIN admin.destinations d ON b.destination_id = d.id
            WHERE 1=1
        """
        params = {}
        if p_status:
            query_str += " AND b.status = :status"
            params["status"] = p_status
        if p_search:
            query_str += " AND (b.full_name ILIKE :search OR b.email ILIKE :search)"
            params["search"] = f"%{p_search}%"
        query_str += " ORDER BY b.id DESC LIMIT :limit OFFSET :offset"
        params["limit"] = p_limit
        params["offset"] = p_offset

        res = await db.execute(text(query_str), params)
        rows = res.fetchall()
        return {"status": 1, "count": len(rows), "data": [dict(r._mapping) for r in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-booking/{id}")
async def get_booking_by_id(id: int, db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(text("""
            SELECT b.*, d.name as destination_name, d.year_label, d.era, d.image_emoji, d.price_inr
            FROM admin.bookings b
            LEFT JOIN admin.destinations d ON b.destination_id = d.id
            WHERE b.id = :id
        """), {"id": id})
        row = res.first()
        if not row:
            raise HTTPException(status_code=404, detail="Booking not found")
        return {"status": 1, "data": dict(row._mapping)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}/pass")
async def get_booking_pass(id: int, db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(text("""
            SELECT b.*, d.name as destination_name, d.year_label, d.era, d.image_emoji, d.price_inr,
                   p.pass_code, p.qr_hash, p.issued_at
            FROM admin.bookings b
            JOIN admin.destinations d ON b.destination_id = d.id
            LEFT JOIN admin.temporal_passes p ON p.booking_id = b.id
            WHERE b.id = :id
        """), {"id": id})
        row = res.first()
        if not row:
            raise HTTPException(status_code=404, detail="Boarding pass not found")
        return {"status": 1, "data": dict(row._mapping)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
