from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import settings

client = AsyncIOMotorClient(settings.mongodb_url)
db = client[settings.mongodb_db]

# Colecciones
organizaciones_collection = db["organizaciones"]
proyectos_collection = db["proyectos"]
participantes_collection = db["participantes"]
