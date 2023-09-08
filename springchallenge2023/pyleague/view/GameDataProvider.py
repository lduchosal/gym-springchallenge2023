from springchallenge2023.pyleague.game.Game import Game
from springchallenge2023.pyleague.view.CellData import CellData
from springchallenge2023.pyleague.view.GlobalViewData import GlobalViewData

class GameDataProvider:

    game: Game

    def __init__(self, game, game_manager):
        self.game = game
        self.game_manager = game_manager

    def get_global_data(self):
        data = GlobalViewData()
        data.cells = [
            CellData(
                q=coord.get_x(),
                r=coord.get_z(),
                richness=cell.get_richness(),
                index=cell.get_index(),
                owner=cell.get_anthill().get_index() if cell.get_anthill() else -1,
                celltype=1 if cell.get_type() == 'EGG' else 2,
                ants=cell.get_ants()
            )
            for cell, coord in self.game.get_board_cells_coord()
        ]
        return data
