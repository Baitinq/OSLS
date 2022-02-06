import sys
import math
from time import sleep

from engine import Engine
from fuel import Fuel
from rocket import Rocket
from atmosphere import Atmosphere
from body import Body
from universe import Universe
from simulation import Simulation

import pygame
from pygame.locals import *

def main(argv):
    rocket = Rocket(name="starship", 
                    rocket_mass=240000, #thrust=245000
                    engine=Engine(name="raptor", thrust=2.3E6, flow_rate=1000), #https://en.wikipedia.org/wiki/SpaceX_Raptor
                    engine_number=33,
                    fuel_type=Fuel(name="methane", energy_density=None),
                    fuel_mass=4000000,
                    drag_coefficient=1.18,
                    cross_sectional_area=(math.pi * (9**2))
                    )
    
    body = Body(name="earth",
                density=5.51,
                radius=6371000,
                atmosphere=Atmosphere(
                                      avg_sea_level_pressure=101325,
                                      molar_mass_air=0.02896,
                                      standard_temp=288.15
                                     )
                )
    
    universe = Universe(name="conventional",
                        G=6.67E-11,
                        plank=None
                        )
    
    simulation = Simulation(universe, body, rocket)

    pygame.init()
    simulation_display = pygame.display.set_mode((400,500))  
    while(True):
        delta = 0.01
        sleep(delta)

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation.rocket.engines_on = not simulation.rocket.engines_on
                elif event.key == pygame.K_LEFT:
                    sys.exit(0)
                elif event.key == pygame.K_RIGHT:
                    sys.exit(0)

        simulation.tick(delta=delta)
        draw_simulation(simulation_display, simulation)

        pygame.display.update()

        #TODO: do max load on rocket so it blows up
        #TODO: display sim info on screen
        #TODO: allow for x movement, speed, accel etc
        #TODO: draw floor, flame
        #TODO: allow multilanguage api for landing algorithms etc

def draw_simulation(simulation_display: type[pygame.Surface], simulation: type[Simulation]) -> None:
        simulation_display.fill(get_color_for_height(simulation.y)) #gradient for atmosphere TODO

        pygame.draw.rect(simulation_display, (0, 125, 255), pygame.Rect(30, 30, 60, 60))
        if simulation.rocket.engines_on:
            pygame.draw.circle(simulation_display, (255, 125, 100), (60, 100), 10)

def get_color_for_height(height: int) -> (int, int, int):
    return (255, 255, 255)

if __name__ == "__main__":
    main(sys.argv)