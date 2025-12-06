from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from .base import PyObjectId

class OrganizacionBase(BaseModel):
    nombre: str
    tipo: str  # "cooperativa", "centro_cultural", "huerta", "asamblea"
    localidad: str
    descripcion: Optional[str] = None

class OrganizacionCreate(OrganizacionBase):
    pass

class Organizacion(OrganizacionBase):
    id: PyObjectId = Field(alias="_id")
    slug: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    proyectos_count: int = 0

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "nombre": "Huerta Colectiva Lonquimay",
                "tipo": "huerta",
                "localidad": "Lonquimay",
                "slug": "huerta-colectiva-lonquimay",
                "proyectos_count": 3
            }
        }
