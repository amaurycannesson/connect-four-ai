from connect_four.app.schemas import ColumnResponse
from connect_four.core import ConnectFour


class ConnectFourService:
    connect_four: ConnectFour

    def __init__(self):
        self.reset()

    def get_columns(self):
        grid = self.connect_four.get_grid()
        return [
            ColumnResponse(cells=cells)
            for cells in list(list(cells) for cells in zip(*grid))
        ]

    def play(self, column_index: int):
        self.connect_four.play(column_index)

    def get_next_disc(self):
        return self.connect_four.get_next_disc()

    def get_winner(self):
        return self.connect_four.get_winner()

    def reset(self):
        self.connect_four = ConnectFour()
