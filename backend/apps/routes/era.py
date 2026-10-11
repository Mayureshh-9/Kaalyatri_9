from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db

router = APIRouter(prefix="/api/eras", tags=["Eras"])

@router.get("/getall-eras")
async def get_all_eras(db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(text("SELECT * FROM admin.eras ORDER BY id ASC"))
        rows = res.fetchall()
        eras = [dict(row._mapping) for row in rows]
        return {"status": 1, "count": len(eras), "data": eras}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
