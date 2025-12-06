import asyncio
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import settings
from backend.database import mongo
from backend.models.organizacion import OrganizacionCreate

async def init_data():
    # Datos de ejemplo para La Pampa
    organizaciones = [
        OrganizacionCreate(
            nombre="Huerta Colectiva Lonquimay",
            tipo="huerta",
            localidad="Lonquimay"
        ),
        OrganizacionCreate(
            nombre="Cooperativa de Agua Eduardo Castex",
            tipo="cooperativa",
            localidad="Eduardo Castex"
        ),
        OrganizacionCreate(
            nombre="Centro Cultural Santa Rosa",
            tipo="centro_cultural",
            localidad="Santa Rosa"
        )
    ]
    
    for org in organizaciones:
        await mongo.organizaciones_collection.insert_one({
            **org.model_dump(),
            "slug": org.nombre.lower().replace(" ", "-").replace("ñ", "n"),
            "_id": str(__import__("bson").ObjectId())
        })
    
    print("✅ Datos iniciales cargados")

if __name__ == "__main__":
    asyncio.run(init_data())
