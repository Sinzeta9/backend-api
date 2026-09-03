from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Backend funcionando"}

def test_db():
    response = client.get("/db-test")

    assert response.status_code == 200
    assert response.json() == {"database": "NucBox K12"}