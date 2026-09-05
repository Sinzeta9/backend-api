import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

if TEST_DATABASE_URL is None:
    raise ValueError("TEST_DATABASE_URL no está configurada")

os.environ["DATABASE_URL"] = TEST_DATABASE_URL


from app.main import app

client = TestClient(app)


@pytest.fixture
def prueba_creada():
    response = client.post(
        "/prueba",
        json={"nombre": "Registro creado por fixture"},
    )

    id_creado = response.json()["id"]

    yield {
        "id": id_creado,
        "nombre": "Registro creado por fixture",
    }

    client.delete(f"/prueba/{id_creado}")


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Backend funcionando"}


def test_db():
    response = client.get("/db-test")

    assert response.status_code == 200
    assert response.json() == {"database": 1}


def test_listar_pruebas(prueba_creada):
    response = client.get("/pruebas")

    assert response.status_code == 200
    assert "pruebas" in response.json()
    assert prueba_creada in response.json()["pruebas"]


def test_crear_prueba():
    response = client.post(
        "/prueba",
        json={"nombre": "Creado desde pytest"},
    )

    id_creado = response.json()["id"]

    try:
        assert response.status_code == 201
        assert response.json()["nombre"] == "Creado desde pytest"
        assert "id" in response.json()
    finally:
        client.delete(f"/prueba/{id_creado}")


def test_actualizar_prueba(prueba_creada):
    response_update = client.put(
        f"/prueba/{prueba_creada['id']}",
        json={"nombre": "Despues de actualizar"},
    )

    assert response_update.status_code == 200
    assert response_update.json()["id"] == prueba_creada["id"]
    assert response_update.json()["nombre"] == "Despues de actualizar"


def test_eliminar_prueba(prueba_creada):
    response_delete = client.delete(f"/prueba/{prueba_creada['id']}")

    assert response_delete.status_code == 204


def test_actualizar_prueba_no_existe():
    response = client.put(
        "/prueba/999999",
        json={"nombre": "No existe"},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Registro no encontrado"}


def test_eliminar_prueba_no_existe():
    response = client.delete("/prueba/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Registro no encontrado"}


def test_crear_prueba_nombre_vacio():
    response = client.post(
        "/prueba",
        json={"nombre": ""},
    )

    assert response.status_code == 422


def test_crear_prueba_nombre_solo_espacios():
    response = client.post(
        "/prueba",
        json={"nombre": "   "},
    )

    assert response.status_code == 422


def test_actualizar_prueba_nombre_vacio():
    response = client.put(
        "/prueba/1",
        json={"nombre": ""},
    )

    assert response.status_code == 422


def test_actualizar_prueba_nombre_solo_espacios():
    response = client.put(
        "/prueba/1",
        json={"nombre": "   "},
    )

    assert response.status_code == 422