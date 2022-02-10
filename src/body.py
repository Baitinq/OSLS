import math

from atmosphere import Atmosphere

class Body():
    def __init__(self, name: str, density: int, radius: int, atmosphere: type[Atmosphere]):
        self.name = name
        self.density = density
        self.radius = radius
        self.atmosphere = atmosphere

    def mass(self):
        body_volume = (4/3) * math.pi * (self.radius**3)
        return body_volume * self.density * 1000

    def g(self, G: float, height: int):
        return (G * self.mass()) / ((self.radius + height) ** 2)


    def __str__(self):
        return "uwu"