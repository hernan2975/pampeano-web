from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .base import PyObjectId

class ProyectoBase(BaseModel):
    nombre: str
    descripcion: str
    tipo: str  # "huerta", "taller", "obra_social", "cultural"
    estado: str = "planificacion"  # planificacion, ejecucion, finalizado
    organizacion_id: PyObjectId

class ProyectoCreate(ProyectoBase):
    pass

class Proyecto(ProyectoBase):
    id: PyObjectId = Field(alias="_id")
    slug: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    participantes_count: int = 0
    recursos: List[str] = []

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nombre": "Huerta Escolar Lonquimay",
                "descripcion": "Huerta orgánica en la escuela primaria",
                "tipo": "huerta",
                "estado": "ejecucion",
                "organizacion_id": "507f1f77bcf86cd799439011",
                "slug": "huerta-escolar-lonquimay",
                "participantes_count": 12
            }
        }
