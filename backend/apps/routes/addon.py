from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db

router = APIRouter(prefix="/api/addons", tags=["Temporal Addons"])

@router.get("/getall-addons")
async def get_all_addons(db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(text("SELECT * FROM admin.temporal_addons ORDER BY id ASC"))
        rows = res.fetchall()
        addons = [dict(row._mapping) for row in rows]
        return {"status": 1, "count": len(addons), "data": addons}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
