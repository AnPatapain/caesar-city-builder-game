from typing import TYPE_CHECKING

from class_types.buildind_types import BuildingTypes
from buildable.buildableCost import buildable_cost

if TYPE_CHECKING:
    from walkers.walker import Walker
    from map_element.tile import Tile
    from buildable.buildable import Buildable


class GameController:
    instance = None

    def __init__(self):
        self.grid: list[list['Tile']] = None
        self.denier = 100000
        self.actual_citizen = 0
        self.max_citizen = 0
        self.walkers: list['Walker'] = []

        self.current_tick = 0
        self.current_day = 0
        self.current_month = 0
        self.current_year = 0
        self.total_day = 0


    def new_building(self, building: 'Buildable'):
        self.denier -= buildable_cost[building.get_build_type()]
        building.on_build_action()

    def has_enough_denier(self, building_type: 'BuildingTypes'):
        return buildable_cost[building_type] <= self.denier

    def get_denier(self):
        return self.denier

    def set_map(self, map):
        self.grid = map

    def get_map(self) -> list[list['Tile']]:
        return self.grid

    def add_walker(self, walker: 'Walker'):
        self.walkers.append(walker)

    def remove_walker(self, walker: 'Walker'):
        self.walkers.remove(walker)

    def update(self):
        self.increase_tick()

    def increase_tick(self):
        if self.current_tick == 50:
            self.increase_day()
            self.current_tick = -1

        self.current_tick += 1

        match self.current_tick:
            case 0:
                pass
            case 1:
                pass


    def increase_day(self):
        if self.current_day == 15:
            self.increase_month()
            self.current_day = -1

        for row in self.grid:
            for tile in row:
                building = tile.get_building()
                if building:
                    building.update_day()

        self.current_day += 1

    def increase_month(self):
        if self.current_month == 12:
            self.increase_year()
            self.current_month = -1

        self.current_month += 1

    def increase_year(self):
        self.current_year += 1


    @staticmethod
    def get_instance():
        if GameController.instance is None:
            GameController.instance = GameController()
        return GameController.instance
