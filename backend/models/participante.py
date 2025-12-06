from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import datetime
from .base import PyObjectId

class ParticipanteBase(BaseModel):
    nombre: str
    apellido: str
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    rol: str = "participante"  # participante, coordinador, técnico
    organizacion_id: PyObjectId

class ParticipanteCreate(ParticipanteBase):
    pass

class Participante(ParticipanteBase):
    id: PyObjectId = Field(alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    proyectos: List[PyObjectId] = []

    class Config:
        populate_by_name = True
