from typing import List
from backend.models.organizacion import Organizacion, OrganizacionCreate
from slugify import slugify

class OrganizacionService:
    def __init__(self, db):
        self.db = db
    
    async def listar(self) -> List[Organizacion]:
        if hasattr(self.db, "organizaciones_collection"):
            cursor = self.db.organizaciones_collection.find()
            return [Organizacion(**doc) async for doc in cursor]
        else:  # SQLite fallback
            async with self.db as conn:
                cursor = await conn.execute("SELECT * FROM organizaciones")
                rows = await cursor.fetchall()
                return [Organizacion(**dict(zip([
                    "id", "nombre", "tipo", "localidad", "created_at"
                ], row))) for row in rows]
    
    async def crear(self, org: OrganizacionCreate) -> Organizacion:
        org_dict = org.model_dump()
        org_dict["slug"] = slugify(org.nombre)
        org_dict["_id"] = str(ObjectId())
        
        if hasattr(self.db, "organizaciones_collection"):
            result = await self.db.organizaciones_collection.insert_one(org_dict)
            org_dict["_id"] = result.inserted_id
        else:  # SQLite
            async with self.db as conn:
                await conn.execute(
                    "INSERT INTO organizaciones (id, nombre, tipo, localidad, created_at) VALUES (?, ?, ?, ?, ?)",
                    (org_dict["_id"], org_dict["nombre"], org_dict["tipo"], 
                     org_dict["localidad"], org_dict.get("created_at", ""))
                )
                await conn.commit()
        
        return Organizacion(**org_dict)
