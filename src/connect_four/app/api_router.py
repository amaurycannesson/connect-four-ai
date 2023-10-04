from typing import List
from fastapi import APIRouter, Depends, status


from .dependencies import get_connect_four_service
from .connect_four_service import ConnectFourService
from .schemas import PlayRequest, ColumnResponse

api_router = APIRouter(prefix="/api", tags=["API"])


@api_router.get(
    "/columns", summary="Get grid columns", response_model=List[ColumnResponse]
)
async def get_columns(
    connect_four: ConnectFourService = Depends(get_connect_four_service),
):
    return connect_four.get_columns()


@api_router.post(
    "/play", summary="Place a disc on the grid", status_code=status.HTTP_201_CREATED
)
async def play(
    request: PlayRequest,
    connect_four: ConnectFourService = Depends(get_connect_four_service),
):
    connect_four.play(request.col_index)
