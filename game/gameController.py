from buildable.buildable import Buildable
from buildable.house import House
from class_types.buildind_types import BuildingTypes
from buildable.buildableCost import buildable_cost



class GameController:
    instance = None
    def __init__(self):
        self.denier = 100000
        self.actual_citizen = 0
        self.max_citizen = 0


    def new_building(self, building: Buildable):
        self.denier -= buildable_cost[building.get_build_type()]
        if isinstance(building, House):
            self.max_citizen += building.get_max_citizen()

    def has_enough_denier(self, building_type: BuildingTypes):
        return buildable_cost[building_type] <= self.denier

    def get_denier(self):
        return self.denier

    @staticmethod
    def get_instance():
        if GameController.instance is None:
            GameController.instance = GameController()
        return GameController.instance
