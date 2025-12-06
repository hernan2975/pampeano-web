from fastapi import APIRouter, Request, Depends, HTTPException
from typing import List
from backend.models.proyecto import Proyecto, ProyectoCreate
from backend.services.proyecto_service import ProyectoService

router = APIRouter(prefix="/proyectos", tags=["proyectos"])

@router.get("/", response_model=List[Proyecto])
async def listar_proyectos(request: Request):
    service = ProyectoService(request.app.state.db)
    return await service.listar()

@router.post("/", response_model=Proyecto)
async def crear_proyecto(proyecto: ProyectoCreate, request: Request):
    service = ProyectoService(request.app.state.db)
    return await service.crear(proyecto)

@router.get("/{proyecto_id}", response_model=Proyecto)
async def obtener_proyecto(proyecto_id: str, request: Request):
    service = ProyectoService(request.app.state.db)
    proyecto = await service.obtener(proyecto_id)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return proyecto
