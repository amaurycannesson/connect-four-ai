import pytest
from connect_four.core import (
    EMPTY_CELL,
    HEIGHT,
    WIDTH,
    AlreadyFilledColumnException,
    Disc,
    ConnectFour,
    DoublePlayException,
    InvalidColumnException,
)


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
    connect_four.place(col_index=0, disc=Disc.RED)

    grid = connect_four.get_grid()

    assert grid[-1][0] == Disc.RED
    assert len([cell for row in grid for cell in row if cell == Disc.RED]) == 1


def test_should_place_a_disc_in_second_last_row_when_placing_two_disc_in_same_col(
    connect_four: ConnectFour,
):
    connect_four.place(col_index=3, disc=Disc.RED)
    connect_four.place(col_index=3, disc=Disc.YELLOW)

    grid = connect_four.get_grid()

    assert grid[-1][3] == Disc.RED
    assert grid[-2][3] == Disc.YELLOW


def test_should_raise_an_error_when_placing_outside_of_the_grid(
    connect_four: ConnectFour,
):
    with pytest.raises(InvalidColumnException):
        connect_four.place(col_index=WIDTH + 2, disc=Disc.YELLOW)


def test_should_raise_an_error_when_placing_in_a_filled_col(connect_four: ConnectFour):
    for i in range(HEIGHT):
        connect_four.place(col_index=0, disc=Disc.RED if i % 2 else Disc.YELLOW)

    with pytest.raises(AlreadyFilledColumnException):
        connect_four.place(col_index=0, disc=Disc.RED if HEIGHT % 2 else Disc.YELLOW)


def test_should_return_no_winner(connect_four: ConnectFour):
    assert connect_four.get_winner() is None


def test_should_raise_an_error_when_playing_2_times_same_disc_color(
    connect_four: ConnectFour,
):
    connect_four.place(col_index=0, disc=Disc.RED)

    with pytest.raises(DoublePlayException):
        connect_four.place(col_index=0, disc=Disc.RED)


def test_red_should_win_when_4_horizontal_red_discs(connect_four: ConnectFour):
    for i in range(4):
        connect_four.place(col_index=i, disc=Disc.RED)
        if i != 3:
            connect_four.place(col_index=i, disc=Disc.YELLOW)

    assert connect_four.get_winner() == Disc.RED


def test_red_should_win_when_4_vertical_red_discs(connect_four: ConnectFour):
    for i in range(4):
        connect_four.place(col_index=0, disc=Disc.RED)
        if i != 3:
            connect_four.place(col_index=1, disc=Disc.YELLOW)

    assert connect_four.get_winner() == Disc.RED


def test_red_should_win_when_4_red_discs_in_top_right_dir(connect_four: ConnectFour):
    connect_four.place(col_index=1, disc=Disc.YELLOW)
    connect_four.place(col_index=0, disc=Disc.RED)
    connect_four.place(col_index=2, disc=Disc.YELLOW)
    connect_four.place(col_index=1, disc=Disc.RED)
    connect_four.place(col_index=2, disc=Disc.YELLOW)
    connect_four.place(col_index=2, disc=Disc.RED)
    connect_four.place(col_index=3, disc=Disc.YELLOW)
    connect_four.place(col_index=3, disc=Disc.RED)
    connect_four.place(col_index=3, disc=Disc.YELLOW)
    connect_four.place(col_index=3, disc=Disc.RED)

    assert connect_four.get_winner() == Disc.RED


def test_red_should_win_when_4_red_discs_in_bottom_right_dir(connect_four: ConnectFour):
    connect_four.place(col_index=2, disc=Disc.YELLOW)
    connect_four.place(col_index=3, disc=Disc.RED)
    connect_four.place(col_index=1, disc=Disc.YELLOW)
    connect_four.place(col_index=2, disc=Disc.RED)
    connect_four.place(col_index=1, disc=Disc.YELLOW)
    connect_four.place(col_index=1, disc=Disc.RED)
    connect_four.place(col_index=0, disc=Disc.YELLOW)
    connect_four.place(col_index=0, disc=Disc.RED)
    connect_four.place(col_index=0, disc=Disc.YELLOW)
    connect_four.place(col_index=0, disc=Disc.RED)

    assert connect_four.get_winner() == Disc.RED
