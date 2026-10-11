from fastapi import APIRouter, Depends, HTTPException, Form, Query
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db
from logger import logger

router = APIRouter(prefix="/api/destinations", tags=["Destinations"])

@router.post("/insert-update-destination")
async def insert_update_destination(
    id: Optional[int] = Form(None),
    name: str = Form(...),
    era: str = Form(...),
    year_label: str = Form(...),
    short_description: str = Form(...),
    description: str = Form(...),
    price_inr: float = Form(...),
    duration_days: Optional[int] = Form(7),
    difficulty: Optional[str] = Form("Moderate"),
    image_emoji: Optional[str] = Form("🌍"),
    accent_color: Optional[str] = Form("#7c4dff"),
    highlights: Optional[str] = Form(None),
    is_featured: Optional[bool] = Form(False),
    created_by: str = Form("system"),
    db: AsyncSession = Depends(get_db)
):
    try:
        # Try stored procedure first
        dest_id = id
        try:
            query = text("""
                SELECT * FROM admin.insert_update_destination(
                    :p_name, :p_era, :p_year_label, :p_short_description, :p_description,
                    :p_price_inr, :p_duration_days, :p_difficulty, :p_image_emoji,
                    :p_accent_color, :p_highlights, :p_is_featured, :p_created_by, :p_id
                )
            """)
            result = await db.execute(query, {
                "p_name": name, "p_era": era, "p_year_label": year_label,
                "p_short_description": short_description, "p_description": description,
                "p_price_inr": price_inr, "p_duration_days": duration_days,
                "p_difficulty": difficulty, "p_image_emoji": image_emoji,
                "p_accent_color": accent_color, "p_highlights": highlights,
                "p_is_featured": is_featured, "p_created_by": created_by, "p_id": id
            })
            row = result.first()
            if row:
                dest_id = row[0]
        except Exception:
            dest_id = None

        if not dest_id:
            # Dual mode fallback: Direct SQL query
            if id:
                await db.execute(text("""
                    UPDATE admin.destinations SET
                        name=:name, era=:era, year_label=:year_label, short_description=:short_description,
                        description=:description, price_inr=:price_inr, duration_days=:duration_days,
                        difficulty=:difficulty, image_emoji=:image_emoji, accent_color=:accent_color,
                        highlights=:highlights, is_featured=:is_featured, updated_date=NOW()
                    WHERE id=:id
                """), {
                    "id": id, "name": name, "era": era, "year_label": year_label,
                    "short_description": short_description, "description": description,
                    "price_inr": price_inr, "duration_days": duration_days,
                    "difficulty": difficulty, "image_emoji": image_emoji,
                    "accent_color": accent_color, "highlights": highlights,
                    "is_featured": is_featured
                })
                dest_id = id
            else:
                res = await db.execute(text("""
                    INSERT INTO admin.destinations (
                        name, era, year_label, short_description, description, price_inr,
                        duration_days, difficulty, image_emoji, accent_color, highlights, is_featured, created_date, updated_date
                    ) VALUES (
                        :name, :era, :year_label, :short_description, :description, :price_inr,
                        :duration_days, :difficulty, :image_emoji, :accent_color, :highlights, :is_featured, NOW(), NOW()
                    ) RETURNING id
                """), {
                    "name": name, "era": era, "year_label": year_label,
                    "short_description": short_description, "description": description,
                    "price_inr": price_inr, "duration_days": duration_days,
                    "difficulty": difficulty, "image_emoji": image_emoji,
                    "accent_color": accent_color, "highlights": highlights,
                    "is_featured": is_featured
                })
                dest_id = res.scalar()

        await db.commit()
        return {"status": 1, "message": "Destination saved successfully", "id": dest_id}
    except Exception as e:
        await db.rollback()
        logger.exception("Error inserting/updating destination")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getall-destinations")
async def get_all_destinations(
    p_limit: int = Query(100, ge=1),
    p_offset: int = Query(0, ge=0),
    p_search: Optional[str] = None,
    p_is_featured: Optional[bool] = None,
    p_era: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        query_str = "SELECT * FROM admin.destinations WHERE 1=1"
        params = {}
        if p_is_featured is True:
            query_str += " AND is_featured = True"
        if p_search:
            query_str += " AND (name ILIKE :search OR description ILIKE :search OR era ILIKE :search)"
            params["search"] = f"%{p_search}%"
        if p_era:
            query_str += " AND (era ILIKE :era)"
            params["era"] = f"%{p_era}%"
        query_str += " ORDER BY is_featured DESC, id ASC LIMIT :limit OFFSET :offset"
        params["limit"] = p_limit
        params["offset"] = p_offset

        res = await db.execute(text(query_str), params)
        rows = res.fetchall()

        return {"status": 1, "count": len(rows), "data": [dict(r._mapping) for r in rows]}
    except Exception as e:
        logger.exception("Error fetching destinations")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-destination/{id}")
async def get_destination_by_id(id: int, db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(text("SELECT * FROM admin.destinations WHERE id = :id"), {"id": id})
        row = res.first()

        if not row:
            raise HTTPException(status_code=404, detail="Destination not found")
        return {"status": 1, "data": dict(row._mapping)}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Get destination failed for ID={id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-destination/{id}")
async def delete_destination(id: int, db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(text("DELETE FROM admin.destinations WHERE id = :id"), {"id": id})
        await db.commit()
        return {"status": 1, "message": "Destination deleted successfully", "id": id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

