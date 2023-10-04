import os

from fastapi import Depends, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .api_router import api_router
from .connect_four_service import ConnectFourService
from .dependencies import get_connect_four_service

app = FastAPI(title="Connect Four App")
templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)

app.include_router(api_router)


@app.get("/", response_class=HTMLResponse)
async def get_index(
    request: Request,
    connect_four_service: ConnectFourService = Depends(get_connect_four_service),
):
    return templates.TemplateResponse(
        "index.html", {"request": request, "grid": connect_four_service.get_columns()}
    )
