from enum import StrEnum
from typing import List, Literal, Optional, TypeGuard, Union

from .exceptions import (
    AlreadyFilledColumnException,
    InvalidColumnException,
)


class Disc(StrEnum):
    RED = "R"
    YELLOW = "Y"


EMPTY_CELL = ""

Cell = Union[Literal[""], Disc]
Grid = List[List[Cell]]

WIDTH = 7
HEIGHT = 6


class ConnectFour:
    _grid: Grid
    _last_play: Disc = Disc.YELLOW

    def __init__(self):
        self._grid = [[EMPTY_CELL] * WIDTH for _ in range(HEIGHT)]

    def get_grid(self) -> Grid:
        return self._grid

    def play(self, col_index: int):
        if col_index < 0 or col_index >= WIDTH:
            raise InvalidColumnException()

        try:
            available_row_index = [row[col_index] for row in self._grid][::-1].index(
                EMPTY_CELL
            )
        except ValueError as value_err:
            raise AlreadyFilledColumnException() from value_err

        played_disc = Disc.RED if self._last_play == Disc.YELLOW else Disc.YELLOW
        self._grid[HEIGHT - 1 - available_row_index][col_index] = played_disc
        self._last_play = played_disc

    def get_winner(self) -> Optional[Disc]:
        def has_four_discs_in_a_row(cell: Cell, row: List[Cell]) -> TypeGuard[Disc]:
            return (
                isinstance(cell, Disc) and cell == row[i + 1] == row[i + 2] == row[i + 3]
            )

        def has_four_discs_in_a_diag(
            cell: Cell, grid: List[List[Cell]], is_going_up: bool
        ) -> TypeGuard[Disc]:
            dir = -1 if is_going_up else 1
            return (
                isinstance(cell, Disc)
                and cell
                == grid[y + 1 * dir][x + 1]
                == grid[y + 2 * dir][x + 2]
                == grid[y + 3 * dir][x + 3]
            )

        for row in self._grid:
            for i in range(WIDTH - 3):
                cur_cell = row[i]
                if has_four_discs_in_a_row(cur_cell, row):
                    return cur_cell

        for col in zip(*self._grid):
            for i in range(HEIGHT - 3):
                cur_cell = col[i]
                if has_four_discs_in_a_row(cur_cell, list(col)):
                    return cur_cell

        for y in range(HEIGHT - 1, HEIGHT - 3, -1):
            for x in range(WIDTH - 3):
                cur_cell = self._grid[y][x]
                if has_four_discs_in_a_diag(cur_cell, self._grid, is_going_up=True):
                    return cur_cell

        for y in range(HEIGHT - 3):
            for x in range(WIDTH - 3):
                cur_cell = self._grid[y][x]
                if has_four_discs_in_a_diag(cur_cell, self._grid, is_going_up=False):
                    return cur_cell
