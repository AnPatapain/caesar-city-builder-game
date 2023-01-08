import pickle
from os import mkdir,path

from game.game_controller import GameController

save_dir = "saved_games/"

def load_game(backup_name):
    path_game = save_dir + backup_name
    if not path.exists(path_game):
        print("game does not exists")
        return None
    file= open(path_game, "rb")
    GameController.get_instance().__dict__ = pickle.load(file)
    file.close()

def save_game(backup_name):
    path_game = save_dir + backup_name
    if not path.exists(save_dir):
        mkdir(save_dir)
    file = open(path_game, "wb")
    pickle.dump(GameController.get_instance().__dict__, file)
    file.close()