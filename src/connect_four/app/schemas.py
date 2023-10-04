from typing import List

from pydantic import BaseModel

from connect_four.core import Cell


class PlayRequest(BaseModel):
    col_index: int


class ColumnResponse(BaseModel):
    cells: List[Cell]
