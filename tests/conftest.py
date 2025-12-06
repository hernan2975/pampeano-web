import pytest
import asyncio
from pathlib import Path
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from backend.config import settings
from backend.database import mongo
from backend.models.organizacion import OrganizacionCreate
from backend.models.proyecto import ProyectoCreate
from backend.models.participante import ParticipanteCreate
from bson import ObjectId

@pytest.fixture(scope="session")
def event_loop():
    """Crear un event loop reutilizable para toda la sesión."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_db():
    """Fixture de base de datos de prueba."""
    # Usar base de datos de prueba separada
    original_db = settings.mongodb_db
    settings.mongodb_db = "pampeano_test"
    
    # Limpiar DB de prueba
    await mongo.db.organizaciones.delete_many({})
    await mongo.db.proyectos.delete_many({})
    await mongo.db.participantes.delete_many({})
    
    yield mongo.db
    
    # Restaurar configuración original
    settings.mongodb_db = original_db

@pytest.fixture
async def sample_organizacion(test_db):
    """Crear una organización de ejemplo para tests."""
    org_data = OrganizacionCreate(
        nombre="Huerta de Prueba",
        tipo="huerta",
        localidad="Santa Rosa",
        descripcion="Organización de prueba para tests"
    )
    
    org_dict = org_data.model_dump()
    org_dict["slug"] = "huerta-de-prueba"
    org_dict["_id"] = ObjectId()
    
    result = await test_db.organizaciones.insert_one(org_dict)
    org_dict["_id"] = result.inserted_id
    
    return org_dict

@pytest.fixture
async def sample_proyecto(test_db, sample_organizacion):
    """Crear un proyecto de ejemplo para tests."""
    proj_data = ProyectoCreate(
        nombre="Proyecto de Prueba",
        descripcion="Proyecto de prueba para tests",
        tipo="huerta",
        estado="planificacion",
        organizacion_id=sample_organizacion["_id"]
    )
    
    proj_dict = proj_data.model_dump()
    proj_dict["slug"] = "proyecto-de-prueba"
    proj_dict["_id"] = ObjectId()
    proj_dict["participantes_count"] = 0
    
    result = await test_db.proyectos.insert_one(proj_dict)
    proj_dict["_id"] = result.inserted_id
    
    return proj_dict

@pytest.fixture
async def test_client():
    """Fixture para cliente de prueba de FastAPI."""
    from fastapi.testclient import TestClient
    from backend.main import app
    
    # Inicializar DB para modo prueba
    app.state.db = mongo
    
    with TestClient(app) as client:
        yield client
