from connect_four.app.schemas import ColumnResponse
from connect_four.core import ConnectFour


class ConnectFourService:
    connect_four: ConnectFour

    def __init__(self):
        self.connect_four = ConnectFour()

    def get_columns(self):
        grid = self.connect_four.get_grid()
        return [
            ColumnResponse(cells=cells)
            for cells in list(list(cells) for cells in zip(*grid))
        ]

    def play(self, column_index: int):
        self.connect_four.play(column_index)
