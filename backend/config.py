import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # MongoDB
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    mongodb_db: str = os.getenv("MONGODB_DB", "pampeano")
    
    # Seguridad
    secret_key: str = os.getenv("SECRET_KEY", "clave-secreta-comunitaria-2025")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24h
    
    # Modo offline
    use_sqlite_fallback: bool = os.getenv("USE_SQLITE_FALLBACK", "false").lower() == "true"
    
    class Config:
        env_file = ".env"

settings = Settings()
