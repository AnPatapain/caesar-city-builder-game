from buildable.house import House
from class_types.buildind_types import BuildingTypes


class SmallTent(House):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, BuildingTypes.SMALL_TENT, build_size=(1, 1),
                         tax=1, desirability=-99, max_citizen=5, prosperity=5)

    def is_upgradable(self) -> bool:
        return self.get_current_tile().get_water_access()

    def conditions_fulfilled(self) -> bool:
        return True

    def upgrade(self):
        #prevent circular import
        from buildable.final.houses.large_tent import LargeTent
        super().upgrade_to(LargeTent)

    def downgrade(self):
        pass