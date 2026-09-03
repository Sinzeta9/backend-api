from fastapi import APIRouter

from app.database import test_connection

router = APIRouter()


@router.get("/db-test")
def db_test():
    nombre = test_connection()
    return {"database": nombre}