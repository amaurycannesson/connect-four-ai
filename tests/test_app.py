from fastapi.testclient import TestClient

from connect_four.app import app
from connect_four.core import EMPTY_CELL, Disc


client = TestClient(app)

import re
from playwright.sync_api import Page, expect


def test_has_title(page: Page):
    page.goto("http://localhost:8000/")

    # Expect a title "to contain" a substring.
    expect(page.locator("css=.disc")).to_have_count(42)


def test_should_return_an_empty_grid():
    response = client.get("/game/grid")
    assert response.status_code == 200
    grid = response.json()
    assert len(grid) == 6
    assert len(grid[0]) == 7
    assert all(cell == EMPTY_CELL for row in grid for cell in row)


def test_should_return_a_grid_with_one_disc_when_adding_one():
    response = client.post("/game/place", json={"col_index": 0, "disc": "R"})
    assert response.status_code == 201
    grid = client.get("/game/grid").json()
    assert grid[-1][0] == Disc.RED.value
