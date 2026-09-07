import logging
import time

from fastapi import FastAPI, Request

from app.logging_config import configurar_logging
from app.routers.auth import router as auth_router
from app.routers.database import router as database_router
from app.routers.users import router as users_router

configurar_logging()

logger = logging.getLogger(
    "app.request",
)

app = FastAPI()

app.include_router(database_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.middleware("http")
async def registrar_peticion(
    request: Request,
    call_next,
):
    inicio = time.perf_counter()

    response = await call_next(request)

    duracion = (time.perf_counter() - inicio) * 1000

    logger.info(
        "%s %s status=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        duracion,
    )

    return response


@app.get("/")
def root():
    return {
        "message": "Backend funcionando",
    }
