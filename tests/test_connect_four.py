import pytest

from connect_four.core import (
    EMPTY_CELL,
    HEIGHT,
    WIDTH,
    AlreadyFilledColumnException,
    ConnectFour,
    Disc,
    InvalidColumnException,
)
from connect_four.core.exceptions import GameOverException


@pytest.fixture
def connect_four():
    return ConnectFour()


def test_should_return_empty_grid_when_no_discs(connect_four: ConnectFour):
    grid = connect_four.get_grid()

    assert len(grid) == 6
    assert len(grid[0]) == 7
    assert all(cell == EMPTY_CELL for row in grid for cell in row)


def test_should_place_a_disc_in_last_row_first_col_when_placing_on_first_row(
    connect_four: ConnectFour,
):
    connect_four.play(col_index=0)

    grid = connect_four.get_grid()

    assert grid[-1][0] == Disc.RED
    assert len([cell for row in grid for cell in row if cell == Disc.RED]) == 1


def test_should_place_a_disc_in_second_last_row_when_placing_two_disc_in_same_col(
    connect_four: ConnectFour,
):
    connect_four.play(col_index=3)
    connect_four.play(col_index=3)

    grid = connect_four.get_grid()

    assert grid[-1][3] == Disc.RED
    assert grid[-2][3] == Disc.YELLOW


def test_should_raise_an_error_when_placing_outside_of_the_grid(
    connect_four: ConnectFour,
):
    with pytest.raises(InvalidColumnException):
        connect_four.play(col_index=WIDTH + 2)


def test_should_raise_an_error_when_placing_in_a_filled_col(connect_four: ConnectFour):
    for i in range(HEIGHT):
        connect_four.play(col_index=0)

    with pytest.raises(AlreadyFilledColumnException):
        connect_four.play(col_index=0)


def test_should_return_no_winner(connect_four: ConnectFour):
    assert connect_four.get_winner() is None


def test_red_should_win_when_4_horizontal_red_discs(connect_four: ConnectFour):
    for i in range(4):
        connect_four.play(col_index=i)
        if i != 3:
            connect_four.play(col_index=i)

    assert connect_four.get_winner() == Disc.RED


def test_red_should_win_when_4_vertical_red_discs(connect_four: ConnectFour):
    for i in range(4):
        connect_four.play(col_index=0)
        if i != 3:
            connect_four.play(col_index=1)

    assert connect_four.get_winner() == Disc.RED


def test_yellow_should_win_when_4_red_discs_in_top_right_dir(connect_four: ConnectFour):
    connect_four.play(col_index=1)
    connect_four.play(col_index=0)
    connect_four.play(col_index=2)
    connect_four.play(col_index=1)
    connect_four.play(col_index=2)
    connect_four.play(col_index=2)
    connect_four.play(col_index=3)
    connect_four.play(col_index=3)
    connect_four.play(col_index=3)
    connect_four.play(col_index=3)

    assert connect_four.get_winner() == Disc.YELLOW


def test_yellow_should_win_when_4_red_discs_in_bottom_right_dir(
    connect_four: ConnectFour,
):
    connect_four.play(col_index=2)
    connect_four.play(col_index=3)
    connect_four.play(col_index=1)
    connect_four.play(col_index=2)
    connect_four.play(col_index=1)
    connect_four.play(col_index=1)
    connect_four.play(col_index=0)
    connect_four.play(col_index=0)
    connect_four.play(col_index=0)
    connect_four.play(col_index=0)

    assert connect_four.get_winner() == Disc.YELLOW


def test_should_return_red_disc_when_asking_first_player_disc(
    connect_four: ConnectFour,
):
    assert connect_four.get_next_disc() == Disc.RED


def test_should_return_yellow_disc_when_playing_first_turn(connect_four: ConnectFour):
    connect_four.play(col_index=0)

    assert connect_four.get_next_disc() == Disc.YELLOW


def test_should_return_7_cols_as_allowed_when_no_disc(connect_four: ConnectFour):
    col_indexes = connect_four.get_free_column_indexes()
    assert len(col_indexes) == 7
    assert all(
        [
            a == b
            for a, b in zip(
                col_indexes,
                [0, 1, 2, 3, 4, 5, 6],
            )
        ]
    )


def test_should_return_only_first_col_when_others_are_filled(connect_four: ConnectFour):
    for i in range(3):
        for _ in range(HEIGHT - 1):
            connect_four.play(i)
    for i in range(3):
        connect_four.play(i)
    for i in range(3, 6):
        for _ in range(HEIGHT - 1):
            connect_four.play(i)
    for i in range(3, 6):
        connect_four.play(i)

    col_indexes = connect_four.get_free_column_indexes()
    assert len(col_indexes) == 1


def test_should_have_no_disc_when_reverting_the_first_play(connect_four: ConnectFour):
    connect_four.play(0)
    connect_four.undo()
    assert all(cell == EMPTY_CELL for row in connect_four.get_grid() for cell in row)


def test_should_have_3_discs_when_reverting_after_4_plays(connect_four: ConnectFour):
    connect_four.play(0)
    connect_four.play(0)
    connect_four.play(0)
    connect_four.play(0)
    connect_four.undo()
    assert (
        len(
            [
                cell
                for row in connect_four.get_grid()
                for cell in row
                if cell != EMPTY_CELL
            ]
        )
        == 3
    )


def test_should_return_red_as_next_player_when_reverting_red_play(
    connect_four: ConnectFour,
):
    connect_four.play(0)
    connect_four.undo()
    assert connect_four.get_next_disc() == Disc.RED


def test_should_return_yellow_as_next_player_when_playing_3_turns_and_reverting_2_turns(
    connect_four: ConnectFour,
):
    connect_four.play(0)
    connect_four.play(0)
    connect_four.play(0)
    connect_four.undo()
    connect_four.undo()
    assert connect_four.get_next_disc() == Disc.YELLOW


def test_should_return_game_over_when_all_columns_are_filled_and_no_winner(
    connect_four: ConnectFour,
):
    for i in range(3):
        for _ in range(HEIGHT - 1):
            connect_four.play(i)
    for i in range(3):
        connect_four.play(i)
    for i in range(3, 6):
        for _ in range(HEIGHT - 1):
            connect_four.play(i)
    for i in range(3, 6):
        connect_four.play(i)
    for _ in range(HEIGHT):
        connect_four.play(WIDTH - 1)

    assert connect_four.is_game_over()
    assert connect_four.get_winner() is None


def test_should_return_game_not_over_when_some_cells_are_empty_and_no_winner(
    connect_four: ConnectFour,
):
    connect_four.play(0)
    assert not connect_four.is_game_over()


def test_should_raise_an_error_when_playing_and_there_is_a_winner(
    connect_four: ConnectFour,
):
    with pytest.raises(GameOverException):
        for i in range(WIDTH):
            for _ in range(HEIGHT):
                connect_four.play(i)
