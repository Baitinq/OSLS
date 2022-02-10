from stage import Stage

class Rocket():
    def __init__(self, name: str, stages: [type[Stage]], payload_mass: int):
        self.name = name
        self.stages = stages
        self.stages_spent = 0
        self.payload_mass = payload_mass

    def current_stage(self) -> type[Stage]:
        return self.stages[0]

    def top_stage(self) -> type[Stage]:
        return self.stages[len(self.stages) - 1] #TODO: drag coef and cross sectional area of top stage

    def perform_stage_separation(self, engines_on: bool):
        if len(self.stages) > 1:
            self.stages.pop(0)
            self.stages_spent += 1
            self.current_stage().engines_on = engines_on

    def total_mass(self):
        total_mass = self.payload_mass
        for stage in self.stages:
            total_mass += stage.total_mass()
        return total_mass
    
    def total_fuel(self):
        fuel_mass = 0
        for stage in self.stages:
            fuel_mass += stage.fuel_mass
        return fuel_mass

    def s_cross_sectional_area(self):
        return self.top_stage().cross_sectional_area

    def s_drag_coefficient(self):
        return self.top_stage().drag_coefficient

    #TODO: IMPLEMENT rocket_x_drag_coefficient() that adds the x drag coefficient of all stages, same with cross sectional area

    def __str__(self):
        return "eue"