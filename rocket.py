from engine import Engine
from fuel import Fuel

class Rocket():
    def __init__(self, name: str, rocket_mass: int, engine: type[Engine], engine_number: int, fuel_type: type[Fuel], fuel_mass: int, drag_coefficient: float, cross_sectional_area: float):
        self.name = name
        self.rocket_mass = rocket_mass
        self.engine = engine
        self.engine_number = engine_number
        self.fuel_type = fuel_type
        self.fuel_mass = fuel_mass
        self.drag_coefficient = drag_coefficient
        self.cross_sectional_area = cross_sectional_area

        self.engines_on = True

    def total_mass(self):
        return self.rocket_mass + self.fuel_mass

    def total_thrust(self):
        if(self.engines_on):
            return self.engine.thrust * self.engine_number
        else:
            return 0

    def total_fuel_used(self, delta: int):
        if(self.engines_on):
            return self.engine.flow_rate * self.engine_number * delta
        else:
            return 0

    def __str__(self):
        return "eue"