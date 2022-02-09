import math

from engine import Engine
from fuel import Fuel

class Stage():
    def __init__(self, name: str, stage_mass: int, engine: type[Engine], engine_number: int, max_engine_gimbaling_angle: int, fuel_type: type[Fuel], fuel_mass: int, drag_coefficient: float, cross_sectional_area: float):
        self.name = name
        self.stage_mass = stage_mass
        self.engine = engine
        self.engine_number = engine_number 
        self.fuel_type = fuel_type
        self.fuel_mass = fuel_mass
        self.drag_coefficient = drag_coefficient
        self.cross_sectional_area = cross_sectional_area
        
        self.max_engine_gimbaling_angle = max_engine_gimbaling_angle
        self.gimbal = 0 #one thing is gimbal another is rocket angle (TODO TOODODODODODODOD)
        self.throttle = 100
        self.engines_on = False

    def total_mass(self):
        return (self.stage_mass + self.fuel_mass)

    def current_thrust(self, g: float) -> (float, float):
        if(self.engines_on and self.fuel_mass > 0):
            total_thrust = self.engine.thrust(self.throttle, g) * self.engine_number
            thrust_x = (math.sin(math.radians(self.gimbal)) * total_thrust)
            thrust_y = (math.cos(math.radians(self.gimbal)) * total_thrust)
            return (thrust_x, thrust_y)
        else:
            return (0, 0)

    def total_fuel_used(self, delta: int):
        if(self.engines_on):
            return self.engine.flow_rate(self.throttle) * self.engine_number * delta
        else:
            return 0

    def convert_y_component_to_total_with_gimbal(self, y_value):
        return math.fabs(y_value / math.cos(math.radians(self.gimbal)))

    #total drag coefficient is just the upper stage
    #engines on is just the lower stage
    #thrust is just the lower stage
    #fuel used is just lower stage
    #when stage separation lower stage jetissoned