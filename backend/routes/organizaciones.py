from fastapi import APIRouter, Request, Depends, HTTPException
from backend.models.organizacion import Organizacion, OrganizacionCreate
from backend.services.organizacion_service import OrganizacionService
from backend.config import settings

router = APIRouter(prefix="/organizaciones", tags=["organizaciones"])

@router.get("/", response_model=list[Organizacion])
async def listar_organizaciones(request: Request):
    service = OrganizacionService(request.app.state.db)
    return await service.listar()

@router.post("/", response_model=Organizacion)
async def crear_organizacion(org: OrganizacionCreate, request: Request):
    service = OrganizacionService(request.app.state.db)
    return await service.crear(org)
