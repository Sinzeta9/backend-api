# Backend API

Proyecto backend de aprendizaje desarrollado con FastAPI y PostgreSQL.

## Tecnologías

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- Psycopg
- PostgreSQL
- Docker
- WSL2
- Git
- Pytest
- Ruff
- uv

## Estructura

```text
backend-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       └── database.py
├── tests/
│   └── test_main.py
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Configuración

El proyecto utiliza variables de entorno para configurar la conexión con PostgreSQL.

El archivo `.env` contiene la configuración local y no se versiona en Git.

El archivo `.env.example` sirve como plantilla y contiene las variables necesarias:

```text
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/devdb
TEST_DATABASE_URL=postgresql+psycopg://USER:PASSWORD@localhost:5432/testdb
```

Cada desarrollador debe crear su propio archivo `.env` utilizando `.env.example` como referencia y sustituir `USER` y `PASSWORD` por sus propios datos.

La aplicación utiliza:

```text
DATABASE_URL → devdb
```

Los tests utilizan:

```text
TEST_DATABASE_URL → testdb
```

De esta forma, las pruebas automatizadas no modifican los datos de la base de datos de desarrollo.

## Ejecutar

Activar el entorno virtual:

```bash
source .venv/bin/activate
```

Iniciar la API:

```bash
uvicorn app.main:app --reload
```

## Endpoints

- `GET /` — comprueba que la API funciona.
- `GET /db-test` — comprueba la conexión con PostgreSQL.
- `POST /prueba` — crea un nuevo registro. Devuelve `201 Created`.
- `GET /pruebas` — muestra todos los registros.
- `PUT /prueba/{id}` — actualiza un registro existente. Devuelve `404` si no existe.
- `DELETE /prueba/{id}` — elimina un registro. Devuelve `204 No Content` si se elimina correctamente y `404` si no existe.

## Validación

Los datos de entrada se validan con Pydantic.

El campo `nombre`:

- No puede estar vacío.
- No puede contener únicamente espacios.
- Elimina automáticamente los espacios al principio y al final.
- Los datos no válidos reciben una respuesta `422 Unprocessable Entity`.

La validación se aplica tanto al crear (`POST`) como al actualizar (`PUT`) registros.

## Documentación

Con la API ejecutándose, Swagger UI está disponible en:

`http://127.0.0.1:8000/docs`

## Tests

