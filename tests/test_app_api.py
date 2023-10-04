from fastapi.testclient import TestClient

from connect_four.app import app
from connect_four.core import EMPTY_CELL, Disc

client = TestClient(app)


def test_api_should_return_an_empty_grid():
    response = client.get("/api/columns")
    assert response.status_code == 200
    cols = response.json()
    assert len(cols) == 7
    assert len(cols[0]["cells"]) == 6
    assert all(cell == EMPTY_CELL for col in cols for cell in col["cells"])


def test_api_should_return_a_grid_with_one_disc_when_adding_one():
    response = client.post("/api/play", json={"col_index": 0})
    assert response.status_code == 201
    cols = client.get("/api/columns").json()
    assert cols[0]["cells"][-1] == Disc.RED.value
