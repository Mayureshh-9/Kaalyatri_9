from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from config import settings

# Create tables (for development - in production use Alembic migrations)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.COMPANY_NAME,
    debug=settings.DEBUG
)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.COMPANY_NAME}"}

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    # Test database connection
    try:
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": str(e)}