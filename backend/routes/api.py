from fastapi import APIRouter, Request
from backend.config import settings

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/health")
async def health_check():
    return {
        "status": "ok",
        "db_type": "sqlite" if settings.use_sqlite_fallback else "mongodb",
        "version": "1.0.0"
    }

@router.get("/config")
async def get_config():
    return {
        "offline_mode": settings.use_sqlite_fallback,
        "max_upload_size": "10MB",
        "allowed_org_types": ["cooperativa", "centro_cultural", "huerta", "asamblea"]
    }
