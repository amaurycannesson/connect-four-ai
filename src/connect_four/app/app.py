from fastapi import APIRouter, FastAPI, status, Depends
from pydantic import BaseModel

from connect_four.core import ConnectFour
from connect_four.core import Grid, Disc


class PlaceDiscRequest(BaseModel):
    col_index: int
    disc: Disc


CONNECT_FOUR = ConnectFour()


def get_connect_four() -> ConnectFour:
    return CONNECT_FOUR


game_router = APIRouter(prefix="/game", tags=["Game"])


@game_router.get("/grid", summary="Get game grid", response_model=Grid)
async def get_grid(connect_four: ConnectFour = Depends(get_connect_four)):
    return connect_four.get_grid()


@game_router.post(
    "/place", summary="Place a disc on the grid", status_code=status.HTTP_201_CREATED
)
async def place_disc(
    request: PlaceDiscRequest, connect_four: ConnectFour = Depends(get_connect_four)
):
    connect_four.place(request.col_index, request.disc)


app = FastAPI(title="Connect Four App")
app.include_router(game_router)
