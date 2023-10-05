import os

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .connect_four_service import ConnectFourService
from .dependencies import get_connect_four_service

app = FastAPI(title="Connect Four App")
templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)


@app.get("/", response_class=HTMLResponse)
async def get_index(
    request: Request,
    connect_four_service: ConnectFourService = Depends(get_connect_four_service),
):
    return templates.TemplateResponse(
        "index.html",
        _build_page_context(request, connect_four_service),
    )


@app.post("/play/{col_index}", response_class=HTMLResponse)
async def play(
    col_index: int,
    request: Request,
    connect_four_service: ConnectFourService = Depends(get_connect_four_service),
):
    connect_four_service.play(col_index)
    return templates.TemplateResponse(
        "partials/game.html",
        _build_page_context(request, connect_four_service),
    )


@app.post("/reset", response_class=HTMLResponse)
async def reset(
    request: Request,
    connect_four_service: ConnectFourService = Depends(get_connect_four_service),
):
    connect_four_service.reset()
    return templates.TemplateResponse(
        "partials/game.html",
        _build_page_context(request, connect_four_service),
    )


def _build_page_context(request: Request, connect_four_service: ConnectFourService):
    return {
        "request": request,
        "grid": connect_four_service.get_columns(),
        "next_disc": connect_four_service.get_next_disc(),
        "winner": connect_four_service.get_winner(),
    }
