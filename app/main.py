from fastapi import FastAPI
from app.database import test_connection
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend funcionando"}

@app.get("/db-test")
def db_test():
    nombre = test_connection()
    return {"database": nombre}
