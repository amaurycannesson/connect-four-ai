from copy import deepcopy
import math
from random import choice
import time
from typing import List, Optional, Self

from connect_four.core import ConnectFour
from connect_four.core.connect_four import Disc


class Node:
    parent: Optional[Self]
    children: List[Self]
    connect_four: ConnectFour
    game_count: int
    win_count: float
    player: Disc
    move: int
    temperature: float = 1.5

    def __init__(self, connect_four: ConnectFour, move: int, parent: Optional[Self]):
        self.children = []
        self.connect_four = connect_four
        self.move = move
        self.player = connect_four.get_next_disc()
        self.parent = parent
        self.game_count = 0
        self.win_count = 0

    def is_leaf(self):
        return len(self.children) == 0

    def get_ucb_value(self) -> float:
        if self.game_count == 0:
            return math.inf
        parent_game_count = self.parent.game_count if self.parent else 0
        return self.win_count / self.game_count + self.temperature * math.sqrt(
            math.log(parent_game_count) / self.game_count
        )


class MonteCarloTreeSearch:
    def next_move(self, connect_four: ConnectFour) -> int:
        root_node = Node(connect_four=connect_four, move=-1, parent=None)
        start = time.process_time()
        while time.process_time() - start < 1:
            selected_node = self._select(root_node)
            if not selected_node.connect_four.is_game_over():
                self._expand(selected_node)
            if not selected_node.is_leaf():
                selected_node = choice(selected_node.children)
            winner = self._simulate(selected_node)
            self._backpropagate(selected_node, winner)
        return min(root_node.children, key=lambda n: n.win_count / n.game_count).move

    def _select(self, node: Node) -> Node:
        selected_node = node
        while not selected_node.is_leaf():
            selected_node = max(selected_node.children, key=lambda n: n.get_ucb_value())
        return selected_node

    def _expand(self, node: Node):
        for move in node.connect_four.get_free_column_indexes():
            connect_four_copy = deepcopy(node.connect_four)
            connect_four_copy.play(move)
            child_node = Node(connect_four=connect_four_copy, move=move, parent=node)
            node.children.append(child_node)

    def _simulate(self, node: Node) -> Optional[Disc]:
        connect_four_copy = deepcopy(node.connect_four)
        while not connect_four_copy.is_game_over():
            moves = connect_four_copy.get_free_column_indexes()
            connect_four_copy.play(choice(moves))
        return connect_four_copy.get_winner()

    def _backpropagate(self, node: Node, winner: Optional[Disc]):
        cur_node = node
        while cur_node is not None:
            cur_node.game_count += 1
            if cur_node.player == winner:
                cur_node.win_count += 1
            cur_node = cur_node.parent
