from fastapi import APIRouter, Depends, HTTPException, Form, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db
from logger import logger

router = APIRouter(prefix="/api/reviews", tags=["Reviews"])

@router.post("/insert-update-review")
async def insert_update_review(
    id: Optional[int] = Form(None),
    destination_id: int = Form(...),
    rating: int = Form(...),
    comment: Optional[str] = Form(None),
    created_by: str = Form("system"),
    db: AsyncSession = Depends(get_db)
):
    try:
        rev_id = id
        try:
            sp_res = await db.execute(text("""
                SELECT * FROM admin.insert_update_review(
                    :p_destination_id, :p_rating, :p_comment, :p_created_by, :p_id
                )
            """), {
                "p_destination_id": destination_id,
                "p_rating": rating,
                "p_comment": comment,
                "p_created_by": created_by,
                "p_id": id
            })
            row = sp_res.first()
            if row:
                rev_id = row[0]
        except Exception:
            rev_id = None

        if not rev_id:
            ins_res = await db.execute(text("""
                INSERT INTO admin.reviews (destination_id, rating, comment, created_by, created_date, updated_date)
                VALUES (:dest_id, :rating, :comment, :created_by, NOW(), NOW())
                RETURNING id
            """), {
                "dest_id": destination_id,
                "rating": rating,
                "comment": comment,
                "created_by": created_by
            })
            rev_id = ins_res.scalar()

        await db.commit()
        return {"status": 1, "message": "Review added successfully", "id": rev_id}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getall-reviews")
async def get_all_reviews(
    p_destination_id: Optional[int] = Query(None),
    p_limit: int = Query(50, ge=1),
    p_offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    try:
        query_str = "SELECT * FROM admin.reviews WHERE 1=1"
        params = {}
        if p_destination_id:
            query_str += " AND destination_id = :dest_id"
            params["dest_id"] = p_destination_id
        query_str += " ORDER BY id DESC LIMIT :limit OFFSET :offset"
        params["limit"] = p_limit
        params["offset"] = p_offset

        res = await db.execute(text(query_str), params)
        rows = res.fetchall()
        return {"status": 1, "count": len(rows), "data": [dict(r._mapping) for r in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
