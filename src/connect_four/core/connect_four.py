from enum import StrEnum
from typing import List, Literal, Optional, Tuple, TypeGuard, Union

from .exceptions import (
    AlreadyFilledColumnException,
    GameOverException,
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
    _last_moves: List[Tuple[Disc, int]]

    def __init__(self):
        self._grid = [[EMPTY_CELL] * WIDTH for _ in range(HEIGHT)]
        self._last_moves = []

    def get_grid(self) -> Grid:
        return self._grid

    def get_next_disc(self) -> Disc:
        return (
            Disc.RED
            if not len(self._last_moves) or self._last_moves[-1][0] == Disc.YELLOW
            else Disc.YELLOW
        )

    def get_free_column_indexes(self) -> List[int]:
        free_col_indexes = []
        for i, col in enumerate(zip(*self._grid)):
            if col.count(EMPTY_CELL) > 0:
                free_col_indexes.append(i)
        return free_col_indexes

    def is_game_over(self) -> bool:
        return (
            all(cell != EMPTY_CELL for row in self._grid for cell in row)
            or self.get_winner() is not None
        )

    def play(self, col_index: int):
        if col_index < 0 or col_index >= WIDTH:
            raise InvalidColumnException()

        if self.is_game_over():
            raise GameOverException()

        try:
            available_row_index = [row[col_index] for row in self._grid][::-1].index(
                EMPTY_CELL
            )
        except ValueError as value_err:
            raise AlreadyFilledColumnException() from value_err

        played_disc = self.get_next_disc()
        self._grid[HEIGHT - 1 - available_row_index][col_index] = played_disc
        self._last_moves.append((played_disc, col_index))

    def undo(self):
        if not len(self._last_moves):
            return

        _last_play, _last_col_index = self._last_moves.pop()
        last_row_index = list(zip(*self._grid))[_last_col_index].index(_last_play)
        self._grid[last_row_index][_last_col_index] = EMPTY_CELL

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

        for y in range(HEIGHT - 1, HEIGHT - 2, -1):
            for x in range(WIDTH - 3):
                cur_cell = self._grid[y][x]
                if has_four_discs_in_a_diag(cur_cell, self._grid, is_going_up=True):
                    return cur_cell

        for y in range(HEIGHT - 3):
            for x in range(WIDTH - 3):
                cur_cell = self._grid[y][x]
                if has_four_discs_in_a_diag(cur_cell, self._grid, is_going_up=False):
                    return cur_cell
