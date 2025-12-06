#!/usr/bin/env python3
"""
Inicializa la base de datos con datos de ejemplo para La Pampa.
Ejecutar una vez después de la instalación.
"""
import asyncio
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import settings
from backend.database import mongo
from backend.models.organizacion import OrganizacionCreate
from backend.models.proyecto import ProyectoCreate
from backend.models.participante import ParticipanteCreate
from bson import ObjectId

async def init_data():
    print("🌾 Inicializando base de datos con datos de ejemplo para La Pampa...")
    
    # Datos de ejemplo: organizaciones
    organizaciones_data = [
        {
            "nombre": "Huerta Colectiva Lonquimay",
            "tipo": "huerta",
            "localidad": "Lonquimay",
            "descripcion": "Huerta orgánica comunitaria con 15 familias participantes."
        },
        {
            "nombre": "Cooperativa de Agua Eduardo Castex",
            "tipo": "cooperativa",
            "localidad": "Eduardo Castex",
            "descripcion": "Gestión comunitaria del servicio de agua potable rural."
        },
        {
            "nombre": "Centro Cultural Santa Rosa",
            "tipo": "centro_cultural",
            "localidad": "Santa Rosa",
            "descripcion": "Espacio para talleres, biblioteca popular y eventos comunitarios."
        },
        {
            "nombre": "Asamblea Vecinal 25 de Mayo",
            "tipo": "asamblea",
            "localidad": "25 de Mayo",
            "descripcion": "Reuniones mensuales para resolver problemáticas barriales."
        }
    ]
    
    # Insertar organizaciones y guardar IDs
    org_ids = {}
    for data in organizaciones_data:
        org = OrganizacionCreate(**data)
        org_dict = org.model_dump()
        org_dict["slug"] = org.nombre.lower().replace(" ", "-").replace("ñ", "n")
        org_dict["_id"] = ObjectId()
        
        if not settings.use_sqlite_fallback:
            result = await mongo.organizaciones_collection.insert_one(org_dict)
            org_ids[org.nombre] = result.inserted_id
        else:
            # Implementación SQLite (simulada para ejemplo)
            org_ids[org.nombre] = str(org_dict["_id"])
        print(f"✅ Organización creada: {org.nombre}")

    # Datos de ejemplo: participantes
    participantes_data = [
        {"nombre": "María", "apellido": "González", "rol": "coordinadora", "organizacion_id": org_ids["Huerta Colectiva Lonquimay"]},
        {"nombre": "Juan", "apellido": "Pérez", "rol": "técnico", "organizacion_id": org_ids["Cooperativa de Agua Eduardo Castex"]},
        {"nombre": "Ana", "apellido": "Rodríguez", "rol": "coordinadora", "organizacion_id": org_ids["Centro Cultural Santa Rosa"]},
        {"nombre": "Carlos", "apellido": "López", "rol": "participante", "organizacion_id": org_ids["Asamblea Vecinal 25 de Mayo"]},
        {"nombre": "Elena", "apellido": "Martínez", "rol": "participante", "organizacion_id": org_ids["Huerta Colectiva Lonquimay"]},
        {"nombre": "Roberto", "apellido": "Sánchez", "rol": "técnico", "organizacion_id": org_ids["Centro Cultural Santa Rosa"]}
    ]
    
    for data in participantes_data:
        part = ParticipanteCreate(**data)
        part_dict = part.model_dump()
        part_dict["_id"] = ObjectId()
        
        if not settings.use_sqlite_fallback:
            await mongo.participantes_collection.insert_one(part_dict)
        # En SQLite se haría en el servicio correspondiente
    print("✅ 6 participantes creados")

    # Datos de ejemplo: proyectos
    proyectos_data = [
        {
            "nombre": "Huerta Escolar Lonquimay",
            "descripcion": "Huerta orgánica en la escuela primaria local.",
            "tipo": "huerta",
            "estado": "ejecucion",
            "organizacion_id": org_ids["Huerta Colectiva Lonquimay"]
        },
        {
            "nombre": "Mantenimiento Red de Agua",
            "descripcion": "Reparación de cañerías en el sector norte.",
            "tipo": "obra_social",
            "estado": "planificacion",
            "organizacion_id": org_ids["Cooperativa de Agua Eduardo Castex"]
        },
        {
            "nombre": "Taller de Tejido",
            "descripcion": "Talleres semanales para adultos mayores.",
            "tipo": "taller",
            "estado": "ejecucion",
            "organizacion_id": org_ids["Centro Cultural Santa Rosa"]
        },
        {
            "nombre": "Mejora Espacio Público",
            "descripcion": "Reacondicionamiento de plaza central.",
            "tipo": "cultural",
            "estado": "finalizado",
            "organizacion_id": org_ids["Asamblea Vecinal 25 de Mayo"]
        }
    ]
    
    for data in proyectos_data:
        proj = ProyectoCreate(**data)
        proj_dict = proj.model_dump()
        proj_dict["slug"] = proj.nombre.lower().replace(" ", "-").replace("ñ", "n")
        proj_dict["_id"] = ObjectId()
        proj_dict["participantes_count"] = 0
        
        if not settings.use_sqlite_fallback:
            await mongo.proyectos_collection.insert_one(proj_dict)
    print("✅ 4 proyectos creados")

    print("\n🎉 Inicialización completada.")
    print("➡️  Ejecute: uvicorn backend.main:app --reload")

if __name__ == "__main__":
    asyncio.run(init_data())
