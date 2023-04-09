from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes


class EntrySign(Buildable):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.ENTRY_FLAG, fire_risk=0, destruction_risk=0)

    def is_destroyable(self, player_id: int):
        return False
