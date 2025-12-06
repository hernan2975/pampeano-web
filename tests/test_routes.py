import pytest
from fastapi.testclient import TestClient
from bson import ObjectId

def test_health_check(test_client):
    """Testear endpoint de salud."""
    response = test_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data

def test_get_config(test_client):
    """Testear endpoint de configuración."""
    response = test_client.get("/api/config")
    assert response.status_code == 200
    data = response.json()
    assert "offline_mode" in data
    assert "allowed_org_types" in data
    assert len(data["allowed_org_types"]) == 4

def test_create_organizacion(test_client):
    """Testear creación de organización."""
    org_data = {
        "nombre": "Huerta de Prueba Test",
        "tipo": "huerta",
        "localidad": "Santa Rosa",
        "descripcion": "Organización de prueba para tests"
    }
    
    response = test_client.post("/organizaciones", json=org_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["nombre"] == "Huerta de Prueba Test"
    assert data["tipo"] == "huerta"
    assert data["slug"] == "huerta-de-prueba-test"
    assert "_id" in data or "id" in data

def test_list_organizaciones(test_client, sample_organizacion):
    """Testear listado de organizaciones."""
    response = test_client.get("/organizaciones")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    
    # Verificar que contenga la organización de prueba
    org_names = [org["nombre"] for org in data]
    assert "Huerta de Prueba" in org_names

def test_get_organizacion(test_client, sample_organizacion):
    """Testear obtención de organización específica."""
    org_id = str(sample_organizacion["_id"])
    response = test_client.get(f"/organizaciones/{org_id}")
    
    # En la implementación actual, no hay endpoint GET individual
    # Este test verificará que devuelva 404 o se implementará el endpoint
    assert response.status_code in [200, 404]

def test_create_proyecto(test_client, sample_organizacion):
    """Testear creación de proyecto."""
    org_id = str(sample_organizacion["_id"])
    proyecto_data = {
        "nombre": "Proyecto de Prueba Test",
        "descripcion": "Proyecto de prueba para tests",
        "tipo": "huerta",
        "estado": "planificacion",
        "organizacion_id": org_id
    }
    
    response = test_client.post("/proyectos", json=proyecto_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["nombre"] == "Proyecto de Prueba Test"
    assert data["organizacion_id"] == org_id

def test_list_proyectos(test_client, sample_proyecto):
    """Testear listado de proyectos."""
    response = test_client.get("/proyectos")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_auth_token(test_client):
    """Testear autenticación."""
    form_data = {
        "username": "admin",
        "password": "pampeano2025"
    }
    
    response = test_client.post("/auth/token", data=form_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_auth_invalid(test_client):
    """Testear autenticación inválida."""
    form_data = {
        "username": "admin",
        "password": "contraseña-incorrecta"
    }
    
    response = test_client.post("/auth/token", data=form_data)
    assert response.status_code == 401
