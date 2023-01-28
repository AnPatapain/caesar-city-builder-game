from typing import TYPE_CHECKING

from buildable.final.structures.granary import Granary
from class_types.buildind_types import BuildingTypes
from class_types.walker_types import WalkerTypes
from game.game_controller import GameController
from walkers.walker import Walker
from enum import Enum

if TYPE_CHECKING:
    from buildable.final.structures.WheatFarm import WheatFarm

class Actions(Enum):
    IDLE = 0
    IN_THE_WAY_TO_FARM = 1
    IN_THE_WAY_TO_GRANARY = 2


class Farm_worker(Walker):
    def __init__(self, associated_building: 'WheatFarm'):
        super().__init__(WalkerTypes.FARM_WORKER, associated_building, roads_only=True)
        self.associated_building: 'WheatFarm' = associated_building
        self.game_controller = GameController.get_instance()
        self.current_action = Actions.IDLE
        self.wheat_in_hand = 0
        self.current_granary_list = [] # list of farm tile


    def find_granary(self) -> Granary:
        grid = self.game_controller.get_map()

        candidates: list[Granary] = []
        for row in grid:
            for tile in row:
                if tile.get_building() and tile.get_building().get_build_type() == BuildingTypes.GRANARY and tile.get_show_tile():
                    candidates.append(tile.get_building())

        spawn_point = self.associated_building.find_adjacent_road()
        for candidate in candidates:
            path = spawn_point.find_path_to(candidate.get_all_building_tiles(), roads_only=True)
            if path:
                return candidate

    def move_wheat_in_hand_to_granary(self, granary):
        from buildable.final.structures.granary import Granary
        granary: Granary = granary
        granary.receive_wheat_from_farm_worker(self.wheat_in_hand)
        self.wheat_in_hand = 0


    def get_food_from_associated_farm(self):
        self.wheat_in_hand = self.associated_building.give_wheat_to_worker()


    def update(self):
        super().update()

        if len(self.current_granary_list) == 0:
            self.get_all_granary_tiles()
        

        if len(self.current_granary_list) != 0:
            if self.current_action == Actions.IDLE:
                if self.current_granary_list[0].get_building():
                    self.navigate_to(self.current_granary_list[0].get_building().get_all_building_tiles())
                    self.current_action = Actions.IN_THE_WAY_TO_GRANARY # update the current action
                else: 
                    self.current_granary_list.pop(0)


    def destination_reached(self):
        # print(self.current_tile.get_building(), self.current_tile.get_show_tile())
        building = self.current_tile.get_building()

        if building and building.get_build_type() == BuildingTypes.GRANARY:
            self.move_wheat_in_hand_to_granary(building)
            self.navigate_to(self.associated_building.get_all_building_tiles()) #back to the farm
            self.current_action = Actions.IN_THE_WAY_TO_FARM
            tile_poped = self.current_granary_list.pop(0)

        elif building and building.get_build_type() == BuildingTypes.WHEAT_FARM:
            self.delete()

    def get_all_granary_tiles(self): 
        from buildable.final.structures.granary import Granary

        grid = self.game_controller.get_map()
        self.current_granary_list = []

        for row in grid:
            for tile in row:
                building = tile.get_building()
                if isinstance(building, Granary) and tile.get_show_tile():
                    # Only add the new granary into current_granary_list if the walker can reach it by road from current tile of walker
                    if len( self.current_tile.find_path_to(building.get_all_building_tiles(), roads_only=True) ) != 0:
                        self.current_granary_list.append(building.get_current_tile())
