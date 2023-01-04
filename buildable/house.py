from abc import ABC, abstractmethod

from buildable.buildable import Buildable
from class_types.buildind_types import BuildingTypes

class House(Buildable, ABC):
    def __init__(self, x: int, y: int, build_type: BuildingTypes, build_size: tuple[int, int],
                 tax: int, desirability: int, max_citizen: int, prosperity: int):
        super().__init__(x, y, build_type, build_size)
        self.max_citizen = max_citizen
        self.current_citizen = 0

        self.has_water = False
        self.tax = tax
        self.desirability = desirability
        self.prosperity = prosperity

    def add_citizen(self, num: int):
        self.current_citizen += num

    def get_citizen(self):
        return self.current_citizen

    def get_max_citizen(self):
        return self.max_citizen

    def get_has_water(self):
        return self.has_water

    def set_has_water(self,has_water):
        self.has_water = has_water

    def get_tax(self):
        return self.tax

    def update_day(self):
        if not self.conditions_fulfilled():
            self.downgrade()
        if self.is_upgradable():
            self.upgrade()

    @abstractmethod
    def is_upgradable(self) -> bool:
        print("FIXME: method is_upgradable is not implemented!")
        return False

    @abstractmethod
    def conditions_fulfilled(self) -> bool:
        print("FIXME: method conditions_fulfilled is not implemented!")
        return True

    @abstractmethod
    def upgrade(self):
        pass

    @abstractmethod
    def downgrade(self):
        pass

    def upgrade_to(self, class_name):
        """
            House auto upgrade (testing)
            Change element:
                - max_citizen
                - tax
                - desirability
                - build_type
            No change element:
                - has_water
                - current_citizen
                - position(x,y)
                - build_size
        """
        next_object = class_name(self.x, self.y)
        self.max_citizen = next_object.max_citizen
        #check citizen number
        if self.max_citizen < self.current_citizen:
                self.current_citizen = self.max_citizen
        self.tax = next_object.tax
        self.desirability = next_object.desirability
        self.build_type = next_object.build_type
        self.__class__ = class_name