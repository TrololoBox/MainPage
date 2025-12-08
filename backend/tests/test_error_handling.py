from fastapi import Body, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from app.main import app


class SamplePayload(BaseModel):
    name: str


@app.get("/tests/http-exception")
def raise_http_exception():
    raise HTTPException(status_code=404, detail="Sample not found")


@app.post("/tests/validation")
def validation_endpoint(payload: SamplePayload = Body(...)):
    return payload


@app.get("/tests/unhandled")
def raise_unhandled_exception():
    raise RuntimeError("Unexpected failure")


def test_http_exception_returns_structured_error():
    client = TestClient(app)

    response = client.get("/tests/http-exception")

    assert response.status_code == 404
    assert response.json() == {
        "code": "not_found",
        "message": "Sample not found",
        "details": None,
    }


def test_validation_error_is_transformed():
    client = TestClient(app)

    response = client.post("/tests/validation", json={"invalid": True})

    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "validation_error"
    assert body["message"] == "Validation error"
    assert isinstance(body["details"], list)
    assert body["details"][0]["loc"][-1] == "name"


def test_unhandled_exception_is_transformed():
    client = TestClient(app)

    response = client.get("/tests/unhandled")

    assert response.status_code == 500
    assert response.json() == {
        "code": "internal_error",
        "message": "Internal server error",
        "details": None,
    }
