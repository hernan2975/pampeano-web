import pytest
from backend.models.organizacion import Organizacion, OrganizacionCreate, OrganizacionBase
from backend.models.proyecto import Proyecto, ProyectoCreate
from backend.models.participante import Participante, ParticipanteCreate
from backend.models.base import PyObjectId
from bson import ObjectId

def test_organizacion_base():
    """Testear modelo base de organización."""
    org = OrganizacionBase(
        nombre="Huerta Test",
        tipo="huerta",
        localidad="Santa Rosa"
    )
    
    assert org.nombre == "Huerta Test"
    assert org.tipo == "huerta"
    assert org.localidad == "Santa Rosa"

def test_organizacion_create():
    """Testear creación de organización."""
    org = OrganizacionCreate(
        nombre="Huerta Test",
        tipo="huerta",
        localidad="Santa Rosa",
        descripcion="Descripción de prueba"
    )
    
    assert org.nombre == "Huerta Test"
    assert org.descripcion == "Descripción de prueba"

def test_organizacion_completa():
    """Testear modelo completo de organización."""
    org_id = ObjectId()
    org = Organizacion(
        _id=org_id,
        nombre="Huerta Test",
        tipo="huerta",
        localidad="Santa Rosa",
        slug="huerta-test",
        proyectos_count=3
    )
    
    assert org.id == org_id
    assert org.slug == "huerta-test"
    assert org.proyectos_count == 3

def test_proyecto_create():
    """Testear creación de proyecto."""
    org_id = ObjectId()
    proyecto = ProyectoCreate(
        nombre="Proyecto Test",
        descripcion="Descripción de prueba",
        tipo="huerta",
        estado="planificacion",
        organizacion_id=org_id
    )
    
    assert proyecto.nombre == "Proyecto Test"
    assert proyecto.organizacion_id == org_id
    assert proyecto.estado == "planificacion"

def test_participante_create():
    """Testear creación de participante."""
    org_id = ObjectId()
    participante = ParticipanteCreate(
        nombre="Juan",
        apellido="Pérez",
        rol="coordinador",
        organizacion_id=org_id
    )
    
    assert participante.nombre == "Juan"
    assert participante.apellido == "Pérez"
    assert participante.rol == "coordinador"

def test_pyobjectid_validation():
    """Testear validación de PyObjectId."""
    # ID válido
    valid_id = str(ObjectId())
    obj_id = PyObjectId(valid_id)
    assert str(obj_id) == valid_id
    
    # ID inválido
    with pytest.raises(ValueError, match="Invalid ObjectId"):
        PyObjectId("invalid-id")
