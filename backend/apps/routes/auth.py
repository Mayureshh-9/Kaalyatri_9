from fastapi import APIRouter, Depends, HTTPException, Form, status
from pydantic import BaseModel, EmailStr
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from db import get_db
from auth import verify_password, get_password_hash, create_access_token, get_current_user
from logger import logger

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class RegisterPayload(BaseModel):
    email: EmailStr
    full_name: str
    password: str
    phone: Optional[str] = None

class LoginPayload(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
async def register_user(payload: RegisterPayload, db: AsyncSession = Depends(get_db)):
    try:
        # Check if email exists
        res = await db.execute(
            text("SELECT id FROM admin.users WHERE email = :email"),
            {"email": payload.email}
        )
        if res.first():
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_pwd = get_password_hash(payload.password)

        # Try stored procedure first
        try:
            sp_res = await db.execute(
                text("""
                    SELECT * FROM admin.insert_update_user(
                        :p_email, :p_full_name, :p_phone, :p_password_hash, :p_is_admin, :p_created_by, NULL
                    )
                """),
                {
                    "p_email": payload.email,
                    "p_full_name": payload.full_name,
                    "p_phone": payload.phone,
                    "p_password_hash": hashed_pwd,
                    "p_is_admin": False,
                    "p_created_by": "system_reg"
                }
            )
            row = sp_res.first()
            user_id = row[0] if row else None
        except Exception:
            user_id = None

        if not user_id:
            # Fallback to direct INSERT
            insert_res = await db.execute(
                text("""
                    INSERT INTO admin.users (email, full_name, phone, password_hash, is_admin, created_date, updated_date)
                    VALUES (:email, :full_name, :phone, :password_hash, False, NOW(), NOW())
                    RETURNING id
                """),
                {
                    "email": payload.email,
                    "full_name": payload.full_name,
                    "phone": payload.phone,
                    "password_hash": hashed_pwd
                }
            )
            user_id = insert_res.scalar()

        await db.commit()

        token = create_access_token({"sub": payload.email, "user_id": user_id})

        return {
            "status": 1,
            "message": "Registration successful",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user_id,
                "email": payload.email,
                "full_name": payload.full_name,
                "phone": payload.phone,
                "is_admin": False
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.exception("Error during user registration")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login")
async def login_user(payload: LoginPayload, db: AsyncSession = Depends(get_db)):
    try:
        res = await db.execute(
            text("SELECT id, email, full_name, phone, password_hash, is_admin FROM admin.users WHERE email = :email"),
            {"email": payload.email}
        )
        row = res.first()
        if not row:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user_dict = dict(row._mapping)
        if not verify_password(payload.password, user_dict["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        token = create_access_token({"sub": user_dict["email"], "user_id": user_dict["id"]})

        return {
            "status": 1,
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user_dict["id"],
                "email": user_dict["email"],
                "full_name": user_dict["full_name"],
                "phone": user_dict["phone"],
                "is_admin": user_dict["is_admin"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error during user login")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return {"status": 1, "data": current_user}
