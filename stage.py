from engine import Engine
from fuel import Fuel

class Stage():
    def __init__(self, stage_mass: int, engine: type[Engine], engine_number: int, fuel_type: type[Fuel], fuel_mass: int, drag_coefficient: float, cross_sectional_area: float):
        self.stage_mass = stage_mass
        self.engine = engine
        self.engine_number = engine_number
        self.fuel_type = fuel_type
        self.fuel_mass = fuel_mass
        self.drag_coefficient = drag_coefficient
        self.cross_sectional_area = cross_sectional_area

    #total drag coefficient is just the upper stage
    #engines on is just the lower stage
    #thrust is just the lower stage
    #fuel used is just lower stage
    #when stage separation lower stage jetissoned