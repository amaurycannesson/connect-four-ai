import pytest

from connect_four.ai import MonteCarloTreeSearch
from connect_four.core import ConnectFour


@pytest.fixture
def connect_four():
    return ConnectFour()


@pytest.fixture
def minimax_ai():
    return MonteCarloTreeSearch()


def test_should_return_a_first_valid_move(
    connect_four: ConnectFour, minimax_ai: MonteCarloTreeSearch
):
    assert 0 <= minimax_ai.next_move(connect_four) < 7


def test_should_play_in_the_last_col_when_all_the_others_are_filled(
    connect_four: ConnectFour, minimax_ai: MonteCarloTreeSearch
):
    for i in range(3):
        for _ in range(6 - 1):
            connect_four.play(i)
    for i in range(3):
        connect_four.play(i)
    for i in range(3, 6):
        for _ in range(6 - 1):
            connect_four.play(i)
    for i in range(3, 6):
        connect_four.play(i)

    assert minimax_ai.next_move(connect_four) == 6


def test_should_play_the_winning_move_when_possible(
    connect_four: ConnectFour, minimax_ai: MonteCarloTreeSearch
):
    for i in range(3):
        for _ in range(4):
            connect_four.play(i)

    assert minimax_ai.next_move(connect_four) == 3
