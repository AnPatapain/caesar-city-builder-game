from abc import ABC
from typing import Optional, TYPE_CHECKING

from events.risk import Risk
from game.game_controller import GameController
from game.textures import Textures

if TYPE_CHECKING:
    from class_types.buildind_types import BuildingTypes
    from walkers.walker import Walker
    from map_element.tile import Tile


class Buildable(ABC):
    def __init__(self, x: int, y: int, build_type: 'BuildingTypes', build_size: tuple[int, int],fire_risk : int ,destruction_risk: int):
        self.build_type = build_type
        self.build_size = build_size

        self.associated_walker: Optional['Walker'] = None

        self.x = x
        self.y = y

        self.risk = Risk(fire_risk, destruction_risk)
        self.count = 0

        self.is_on_fire = False

    def get_current_tile(self) -> 'Tile':
        grid = GameController.get_instance().get_map()
        return grid[self.x][self.y]

    def is_destroyable(self):
        return True

    def get_texture(self):
        return Textures.get_texture(self.build_type, texture_number=self.get_current_tile().random_texture_number)

    def get_delete_texture(self):
        return Textures.get_delete_texture(self.build_type, texture_number=self.get_current_tile().random_texture_number)

    def get_build_texture(self):
        return self.get_texture()

    def get_building_size(self):
        return self.build_size

    def get_build_type(self):
        return self.build_type

    def on_build_action(self):
        print("FIXME: method on_build_action not implemented!")
        pass

    def destroy(self):
        if self.associated_walker:
            self.associated_walker.delete()
        pass

    def new_walker(self):
        print("FIXME: method new_walker not implemented!")
        pass

    def update_tick(self):
        pass

    def update_day(self):
        pass

    def to_ruin(self):

        from buildable.final.buildable.ruin import Ruin
        next_object = Ruin(self.x, self.y)
        self.build_type = next_object.build_type
        self.__class__ = Ruin

    def get_risk(self) -> Risk:
        return self.risk