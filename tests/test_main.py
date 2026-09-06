import os

import pytest
from alembic.config import Config
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import delete

from alembic import command

load_dotenv()


def configurar_base_datos_tests():
    test_database_url = os.getenv("TEST_DATABASE_URL")

    if test_database_url is None:
        raise ValueError("TEST_DATABASE_URL no está configurada")

    os.environ["DATABASE_URL"] = test_database_url


def migrar_base_datos_tests():
    alembic_config = Config("alembic.ini")
    command.upgrade(alembic_config, "head")


configurar_base_datos_tests()
migrar_base_datos_tests()

from app.database import SessionLocal
from app.main import app
from app.models import Usuario
from app.security import verificar_password

client = TestClient(app)


@pytest.fixture(autouse=True)
def limpiar_usuarios():
    with SessionLocal() as db:
        db.execute(delete(Usuario))
        db.commit()

    yield

    with SessionLocal() as db:
        db.execute(delete(Usuario))
        db.commit()


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
        "descripcion": None,
        "categoria_id": None,
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


def test_crear_categoria():
    response = client.post(
        "/categorias",
        json={"nombre": "Backend"},
    )

    assert response.status_code == 201
    assert response.json()["nombre"] == "Backend"
    assert "id" in response.json()


def test_listar_categorias():
    response_crear = client.post(
        "/categorias",
        json={"nombre": "Data"},
    )

    categoria = response_crear.json()

    response = client.get("/categorias")

    assert response.status_code == 200
    assert "categorias" in response.json()
    assert categoria in response.json()["categorias"]


def test_crear_prueba_con_categoria():
    response_categoria = client.post(
        "/categorias",
        json={"nombre": "Cloud"},
    )

    categoria_id = response_categoria.json()["id"]

    response = client.post(
        "/prueba",
        json={
            "nombre": "Docker",
            "descripcion": "Contenedores",
            "categoria_id": categoria_id,
        },
    )

    assert response.status_code == 201
    assert response.json()["nombre"] == "Docker"
    assert response.json()["descripcion"] == "Contenedores"
    assert response.json()["categoria_id"] == categoria_id


def test_listar_pruebas_de_categoria():
    response_categoria = client.post(
        "/categorias",
        json={"nombre": "Python"},
    )

    categoria_id = response_categoria.json()["id"]

    response_prueba = client.post(
        "/prueba",
        json={
            "nombre": "FastAPI",
            "descripcion": "API backend",
            "categoria_id": categoria_id,
        },
    )

    prueba = response_prueba.json()

    response = client.get(
        f"/categorias/{categoria_id}/pruebas",
    )

    assert response.status_code == 200
    assert prueba in response.json()["pruebas"]


def test_crear_prueba_categoria_no_existe():
    response = client.post(
        "/prueba",
        json={
            "nombre": "Invalida",
            "categoria_id": 999999,
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Categoría no encontrada",
    }


def test_listar_pruebas_categoria_no_existe():
    response = client.get(
        "/categorias/999999/pruebas",
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Categoría no encontrada",
    }


def test_crear_usuario():
    response = client.post(
        "/usuarios",
        json={
            "nombre": "Bea",
            "email": "bea@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 201
    assert response.json()["nombre"] == "Bea"
    assert response.json()["email"] == "bea@example.com"
    assert "id" in response.json()
    assert "password" not in response.json()
    assert "password_hash" not in response.json()


def test_listar_usuarios():
    response = client.get("/usuarios")

    assert response.status_code == 200
    assert "usuarios" in response.json()


def test_obtener_usuario():
    response_crear = client.post(
        "/usuarios",
        json={
            "nombre": "Usuario individual",
            "email": "individual@example.com",
            "password": "Password123!",
        },
    )

    usuario_id = response_crear.json()["id"]

    response = client.get(
        f"/usuarios/{usuario_id}",
    )

    assert response.status_code == 200
    assert response.json()["id"] == usuario_id
    assert response.json()["email"] == "individual@example.com"
    assert "password_hash" not in response.json()


def test_usuario_email_invalido():
    response = client.post(
        "/usuarios",
        json={
            "nombre": "Email malo",
            "email": "esto-no-es-un-email",
            "password": "Password123!",
        },
    )

    assert response.status_code == 422


def test_usuario_no_existe():
    response = client.get(
        "/usuarios/999999",
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Usuario no encontrado",
    }


def test_usuario_email_duplicado():
    email = "duplicado@example.com"

    client.post(
        "/usuarios",
        json={
            "nombre": "Primero",
            "email": email,
            "password": "Password123!",
        },
    )

    response = client.post(
        "/usuarios",
        json={
            "nombre": "Segundo",
            "email": email,
            "password": "Password456!",
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "El email ya está registrado",
    }


def test_password_se_guarda_hasheado():
    response = client.post(
        "/usuarios",
        json={
            "nombre": "Hash test",
            "email": "hash@example.com",
            "password": "Password123!",
        },
    )

    usuario_id = response.json()["id"]

    with SessionLocal() as db:
        usuario = db.get(Usuario, usuario_id)

        assert usuario is not None
        assert usuario.password_hash != "Password123!"
        assert verificar_password(
            "Password123!",
            usuario.password_hash,
        )


def crear_usuario_para_login(
    email: str = "login@example.com",
):
    return client.post(
        "/usuarios",
        json={
            "nombre": "Usuario login",
            "email": email,
            "password": "Password123!",
        },
    )


def test_login_correcto():
    crear_usuario_para_login()

    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_password_incorrecto():
    crear_usuario_para_login()

    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "PasswordIncorrecto",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Credenciales incorrectas",
    }


def test_login_usuario_no_existe():
    response = client.post(
        "/auth/login",
        json={
            "email": "nadie@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Credenciales incorrectas",
    }


def test_auth_me():
    crear_usuario_para_login()

    response_login = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "Password123!",
        },
    )

    token = response_login.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert response.json()["email"] == "login@example.com"
    assert "password" not in response.json()
    assert "password_hash" not in response.json()


def test_auth_me_sin_token():
    response = client.get("/auth/me")

    assert response.status_code == 401
    assert response.json() == {
        "detail": "No autenticado",
    }


def test_auth_me_token_invalido():
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer token-invalido",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "detail": "Token inválido o expirado",
    }
