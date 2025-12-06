from typing import List, Optional
from backend.models.proyecto import Proyecto, ProyectoCreate
from slugify import slugify
from bson import ObjectId

class ProyectoService:
    def __init__(self, db):
        self.db = db
    
    async def listar(self) -> List[Proyecto]:
        if hasattr(self.db, "proyectos_collection"):
            cursor = self.db.proyectos_collection.find()
            return [Proyecto(**doc) async for doc in cursor]
        else:  # SQLite
            async with self.db as conn:
                cursor = await conn.execute("SELECT * FROM proyectos")
                rows = await cursor.fetchall()
                return [Proyecto(**dict(zip([
                    "id", "nombre", "descripcion", "tipo", "estado", 
                    "organizacion_id", "slug", "created_at", "participantes_count"
                ], row))) for row in rows]
    
    async def crear(self, proyecto: ProyectoCreate) -> Proyecto:
        proyecto_dict = proyecto.model_dump()
        proyecto_dict["slug"] = slugify(proyecto.nombre)
        proyecto_dict["_id"] = str(ObjectId())
        proyecto_dict["participantes_count"] = 0
        
        if hasattr(self.db, "proyectos_collection"):
            result = await self.db.proyectos_collection.insert_one(proyecto_dict)
            proyecto_dict["_id"] = result.inserted_id
        else:  # SQLite
            async with self.db as conn:
                await conn.execute(
                    """INSERT INTO proyectos 
                    (id, nombre, descripcion, tipo, estado, organizacion_id, slug, created_at, participantes_count) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (proyecto_dict["_id"], proyecto_dict["nombre"], proyecto_dict["descripcion"],
                     proyecto_dict["tipo"], proyecto_dict["estado"], str(proyecto_dict["organizacion_id"]),
                     proyecto_dict["slug"], proyecto_dict.get("created_at", ""), 0)
                )
                await conn.commit()
        
        return Proyecto(**proyecto_dict)
    
    async def obtener(self, proyecto_id: str) -> Optional[Proyecto]:
        if hasattr(self.db, "proyectos_collection"):
            doc = await self.db.proyectos_collection.find_one({"_id": ObjectId(proyecto_id)})
            return Proyecto(**doc) if doc else None
        else:  # SQLite
            async with self.db as conn:
                cursor = await conn.execute(
                    "SELECT * FROM proyectos WHERE id = ?", (proyecto_id,)
                )
                row = await cursor.fetchone()
                return Proyecto(**dict(zip([
                    "id", "nombre", "descripcion", "tipo", "estado", 
                    "organizacion_id", "slug", "created_at", "participantes_count"
                ], row))) if row else None
