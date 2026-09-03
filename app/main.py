from fastapi import FastAPI

from app.routers.database import router as database_router

app = FastAPI()

app.include_router(database_router)


@app.get("/")
def root():
    return {"message": "Backend funcionando"}