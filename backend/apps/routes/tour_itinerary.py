from fastapi import APIRouter, Depends, HTTPException, Form, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db

router = APIRouter(prefix="/api/itineraries", tags=["Tour Itineraries"])

@router.get("/getall-tour-itineraries")
async def get_all_tour_itineraries(
    p_destination_id: Optional[int] = Query(None),
    p_limit: int = Query(50, ge=1),
    db: AsyncSession = Depends(get_db)
):
    try:
        query_str = "SELECT * FROM admin.tour_itineraries WHERE 1=1"
        params = {}
        if p_destination_id:
            query_str += " AND destination_id = :dest_id"
            params["dest_id"] = p_destination_id
        query_str += " ORDER BY day_number ASC LIMIT :limit"
        params["limit"] = p_limit

        res = await db.execute(text(query_str), params)
        rows = res.fetchall()
        return {"status": 1, "count": len(rows), "data": [dict(r._mapping) for r in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/insert-update-tour-itinerary")
async def insert_update_tour_itinerary(
    id: Optional[int] = Form(None),
    destination_id: int = Form(...),
    day_number: int = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    created_by: str = Form("system"),
    db: AsyncSession = Depends(get_db)
):
    try:
        if id:
            await db.execute(text("""
                UPDATE admin.tour_itineraries SET
                    destination_id=:dest_id, day_number=:day_num, title=:title, description=:desc, updated_date=NOW()
                WHERE id=:id
            """), {"id": id, "dest_id": destination_id, "day_num": day_number, "title": title, "desc": description})
            itin_id = id
        else:
            res = await db.execute(text("""
                INSERT INTO admin.tour_itineraries (destination_id, day_number, title, description, created_date, updated_date)
                VALUES (:dest_id, :day_num, :title, :desc, NOW(), NOW())
                RETURNING id
            """), {"dest_id": destination_id, "day_num": day_number, "title": title, "desc": description})
            itin_id = res.scalar()

        await db.commit()
        return {"status": 1, "message": "Itinerary saved successfully", "id": itin_id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
