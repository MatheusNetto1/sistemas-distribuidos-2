from app.main import app

from fastapi import status
from fastapi.testclient import TestClient


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
