from fastapi import APIRouter, Depends, HTTPException, Form, Query
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db
from logger import logger

router = APIRouter(prefix="/api/users", tags=["Users"])

@router.post("/insert-update-user")
async def insert_update_user(
    id: Optional[int] = Form(None),
    email: str = Form(...),
    full_name: str = Form(...),
    phone: Optional[str] = Form(None),
    password_hash: str = Form(...),
    is_admin: Optional[bool] = Form(False),
    created_by: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    try:
        query = text("""
            SELECT * FROM admin.insert_update_user(
                :p_email,
                :p_full_name,
                :p_phone,
                :p_password_hash,
                :p_is_admin,
                :p_created_by,
                :p_id
            )
        """)

        result = await db.execute(query, {
            "p_email": email,
            "p_full_name": full_name,
            "p_phone": phone,
            "p_password_hash": password_hash,
            "p_is_admin": is_admin,
            "p_created_by": created_by,
            "p_id": id
        })

        row = result.first()
        if not row:
            logger.warning(f"No DB response for Insert/Update | Email={email}")
            raise HTTPException(status_code=500, detail="No result returned from function")

        await db.commit()

        logger.info(
            f"{'Updated' if id else 'Inserted'} User | "
            f"Email={email} | CreatedBy={created_by}"
        )

        custom_message = "User created successfully" if id is None else "User updated successfully"
        return {"status": 1, "message": custom_message, "id": row[0]}

    except Exception as e:
        await db.rollback()
        logger.exception(f"Insert/Update user failed | Email={email} | User={created_by}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/getall-users")
async def get_all_users(
    p_limit: int = Query(10, ge=1),
    p_offset: int = Query(0, ge=0),
    p_search: str = None,
    db: AsyncSession = Depends(get_db)
):
    try:
        query = text("SELECT * FROM admin.get_all_users(:p_limit, :p_offset, :p_search)")
        result = await db.execute(query, {
            "p_limit": p_limit,
            "p_offset": p_offset,
            "p_search": p_search
        })
        rows = result.fetchall()
        logger.info(f"Fetched users | Count={len(rows)} | Limit={p_limit} | Offset={p_offset}")
        return {"status": 1, "count": len(rows), "data": [dict(row._mapping) for row in rows]}
    except Exception as e:
        logger.exception("Error fetching users with pagination")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get-user/{id}")
async def get_user_by_id(id: int, db: AsyncSession = Depends(get_db)):
    try:
        query = text("SELECT * FROM admin.get_user_by_id(:p_user_id)")
        result = await db.execute(query, {"p_user_id": id})
        row = result.first()

        if not row:
            logger.warning(f"No User found | UserID={id}")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"Fetched User | UserID={id}")
        return {"status": 1, "data": dict(row._mapping)}
    except Exception as e:
        logger.exception(f"Get user failed | UserID={id}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete-user/{id}")
async def delete_user(
    id: int,
    deleted_by: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        if deleted_by == 0:
            logger.warning(f"Invalid deleted_by user for UserID={id}")
            raise HTTPException(400, "deleted_by is invalid")

        query = text("SELECT * FROM admin.delete_user(:p_id, :p_deleted_by)")
        result = await db.execute(query, {
            "p_id": id,
            "p_deleted_by": deleted_by
        })

        row = result.first()
        if not row:
            logger.warning(f"No DB response on delete | UserID={id}")
            raise HTTPException(500, "No result returned from function")

        await db.commit()
        logger.info(f"Deleted User | UserID={id} | DeletedBy={deleted_by}")

        return JSONResponse(
            status_code=200,
            content={
                "status": 1,
                "message": row[0],
                "id": id
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.exception(f"Delete user failed | UserID={id} | DeletedBy={deleted_by}")
        raise HTTPException(status_code=500, detail="Failed to delete user")
