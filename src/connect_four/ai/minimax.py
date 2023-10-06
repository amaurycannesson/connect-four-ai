import math
from typing import List, TypeGuard
from connect_four.core import ConnectFour, Disc
from connect_four.core.connect_four import HEIGHT, WIDTH, Cell


class MinimaxAI:
    def __init__(self, max_depth: int = 3):
        self.max_depth = max_depth

    def next_move(self, connect_four: ConnectFour) -> int:
        best_move = 1
        best_score = -math.inf
        for move in connect_four.get_free_column_indexes():
            ai_disc = connect_four.get_next_disc()
            connect_four.play(move)
            score = self._minimax(
                connect_four, ai_disc, is_max=False, depth=self.max_depth
            )
            connect_four.undo()
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def _minimax(
        self,
        connect_four: ConnectFour,
        max_disc: Disc,
        is_max: bool,
        depth: int,
        alpha: float = -math.inf,
        beta: float = math.inf,
    ) -> float:
        if connect_four.is_game_over() or depth == 0:
            return self._evaluate(connect_four, max_disc)

        if is_max:
            best_score = -math.inf
            for move in connect_four.get_free_column_indexes():
                connect_four.play(move)
                score = self._minimax(
                    connect_four,
                    max_disc,
                    is_max=False,
                    depth=depth - 1,
                    alpha=alpha,
                    beta=beta,
                )
                connect_four.undo()
                best_score = max(best_score, score)
                alpha = max(alpha, score)
                if beta <= alpha:
                    break
            return best_score

        best_score = math.inf
        for move in connect_four.get_free_column_indexes():
            connect_four.play(move)
            score = self._minimax(
                connect_four,
                max_disc,
                is_max=True,
                depth=depth - 1,
                alpha=alpha,
                beta=beta,
            )
            connect_four.undo()
            best_score = min(best_score, score)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score

    def _evaluate(self, connect_four: ConnectFour, max_disc: Disc) -> float:
        """
        +1 / -1 for each line of 3 discs
        +10 / -10 for winning/losing
        0 for a draw
        """

        def count_three_discs_lines(disc: Disc):
            def has_three_discs_in_a_row(cell: Cell, row: List[Cell]) -> TypeGuard[Disc]:
                return cell == disc and cell == row[i + 1] == row[i + 2]

            def has_three_discs_in_a_diag(
                cell: Cell, grid: List[List[Cell]], is_going_up: bool
            ) -> TypeGuard[Disc]:
                dir = -1 if is_going_up else 1
                return (
                    cell == disc
                    and cell == grid[y + 1 * dir][x + 1] == grid[y + 2 * dir][x + 2]
                )

            count = 0
            for row in connect_four.get_grid():
                for i in range(WIDTH - 2):
                    cur_cell = row[i]
                    if has_three_discs_in_a_row(cur_cell, row):
                        count += 1

            for col in zip(*connect_four.get_grid()):
                for i in range(HEIGHT - 2):
                    cur_cell = col[i]
                    if has_three_discs_in_a_row(cur_cell, list(col)):
                        count += 1

            for y in range(HEIGHT - 1, HEIGHT - 2, -1):
                for x in range(WIDTH - 2):
                    cur_cell = connect_four.get_grid()[y][x]
                    if has_three_discs_in_a_diag(
                        cur_cell, connect_four.get_grid(), is_going_up=True
                    ):
                        count += 1

            for y in range(HEIGHT - 2):
                for x in range(WIDTH - 2):
                    cur_cell = connect_four.get_grid()[y][x]
                    if has_three_discs_in_a_diag(
                        cur_cell, connect_four.get_grid(), is_going_up=False
                    ):
                        count += 1
            return count

        min_disc = Disc.RED if max_disc == Disc.YELLOW else Disc.YELLOW
        min_disc_count = count_three_discs_lines(min_disc) * -1
        max_disc_count = count_three_discs_lines(max_disc)
        win = self._evaluate_win(connect_four, max_disc)
        return min_disc_count + max_disc_count + win * 10

    def _evaluate_win(self, connect_four: ConnectFour, max_disc: Disc) -> float:
        """
        going all the way down to the final state is too slow
        """
        if connect_four.get_winner() is None:
            return 0
        elif connect_four.get_winner() == max_disc:
            return 1
        else:
            return -1
