from fastapi.testclient import TestClient

from app.main import app
client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Backend funcionando"}

def test_db():
    response = client.get("/db-test")

    assert response.status_code == 200
    assert response.json() == {"database": "NucBox K12"}

def test_listar_pruebas():
    response = client.get("/pruebas")

    assert response.status_code == 200
    assert "pruebas" in response.json()

def test_crear_prueba():
    response = client.post(
        "/prueba",
        json={"nombre": "Creado desde pytest"},
    )

    assert response.status_code == 200
    assert response.json()["nombre"] == "Creado desde pytest"
    assert "id" in response.json()

    id_creado = response.json()["id"]

    response_delete = client.delete(f"/prueba/{id_creado}")

    assert response_delete.status_code == 200
    assert response_delete.json()["id"] == id_creado

def test_actualizar_prueba():
    response_create = client.post(
        "/prueba",
        json={"nombre": "Antes de actualizar"},
    )

    id_creado = response_create.json()["id"]

    response_update = client.put(
        f"/prueba/{id_creado}",
        json={"nombre": "Despues de actualizar"},
    )

    assert response_update.status_code == 200
    assert response_update.json()["id"] == id_creado
    assert response_update.json()["nombre"] == "Despues de actualizar"

    client.delete(f"/prueba/{id_creado}")

def test_eliminar_prueba():
    response_create = client.post(
        "/prueba",
        json={"nombre": "Registro para eliminar"},
    )

    id_creado = response_create.json()["id"]

    response_delete = client.delete(f"/prueba/{id_creado}")

    assert response_delete.status_code == 200
    assert response_delete.json()["id"] == id_creado
    assert response_delete.json()["nombre"] == "Registro para eliminar"
    assert response_delete.json()["mensaje"] == "Registro eliminado"


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