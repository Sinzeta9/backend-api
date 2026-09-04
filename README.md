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
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       └── database.py
├── tests/
│   └── test_main.py
├── .gitignore
├── README.md
└── requirements.txt
```

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
- `POST /prueba` — crea un nuevo registro.
- `GET /pruebas` — muestra todos los registros.

## Documentación

Con la API ejecutándose, Swagger UI está disponible en:

`http://127.0.0.1:8000/docs`

## Tests

Ejecutar los tests:

```bash
python -m pytest
```