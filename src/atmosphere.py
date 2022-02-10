import math

class Atmosphere():
    def __init__(self, avg_sea_level_pressure: int, molar_mass_air: float, standard_temp: float):
        self.avg_sea_level_pressure = avg_sea_level_pressure
        self.molar_mass_air = molar_mass_air
        self.standard_temp = standard_temp

    #https://math24.net/barometric-formula.html
    def density_at_height(self, height: int, g: float) -> None:
        R = 8.3144598 #universal gas constant
        pressure = self.avg_sea_level_pressure * math.e ** (-(self.molar_mass_air * g * height)/(R * self.standard_temp))
        density = pressure / (R * 10000)
        return density