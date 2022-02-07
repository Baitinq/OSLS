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
    clock = pygame.time.Clock()

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 720

    simulation_display = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    while(True):
        draw_simulation(simulation_display, simulation)
        pygame.display.update()

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit()
                else:
                    handle_key_press(simulation, event.key)

        delta = clock.tick(60) / 1000 #60fps #are we using delta in the simulation tick everywhere needed?
        print("delta: " + str(delta))
        simulation.tick(delta=delta)

        #TODO: draw floor, flame
        #TODO: add support for rocket stages
        #TODO: do max load on rocket so it blows up
        #TODO: allow for x movement, speed, accel etc
        #TODO: allow multilanguage api for landing algorithms etc

def draw_simulation(simulation_display: type[pygame.Surface], simulation: type[Simulation]) -> None:

        font = pygame.font.SysFont("Comic Sans MS", 30)
        
        #draw background
        def get_color_for_height(height: int) -> (int, int, int):
            return (255, 255, 255)
        
        simulation_display.fill(get_color_for_height(simulation.y)) #gradient for atmosphere TODO

        #draw stats text
        simulation_display.blit(font.render("Altitude: {:.0f}m".format(simulation.y), False, (0, 0, 0)),(0,0))
        simulation_display.blit(font.render("Speed: {:.0f}m/s".format(simulation.speed_y), False, (0, 0, 0)),(0,40))
        simulation_display.blit(font.render("Acceleration: {:.2f}m/s2".format(simulation.acceleration_y), False, (0, 0, 0)),(0,80))
        simulation_display.blit(font.render("Fuel: {:.0f}kg".format(simulation.rocket.fuel_mass), False, (0, 0, 0)),(0,120))

        #draw rocket
        rocket_height = 90
        rocket_width = 60

        def calculate_rocket_y_based_on_y_speed_accel(display_height: int, rocket_height: int, speed_y: float, accel_y: float) -> int:
            top = display_height / 5 - (rocket_height / 2) #in the case we are accelerating positively
            bottom = display_height - (top * 2)

            return bottom
            
        def calculate_rocket_x_based_on_x_speed_accel(display_width: int, rocket_width: int, speed_x: float, accel_x: float) -> int:
            return display_width / 2 - (rocket_width / 2)

        rocket_x = calculate_rocket_x_based_on_x_speed_accel(simulation_display.get_width(), rocket_width, None, None)
        rocket_y = calculate_rocket_y_based_on_y_speed_accel(simulation_display.get_height(), rocket_height, simulation.speed_y, simulation.acceleration_y)

        rocket_color = (0, 125, 255)

        flame_radius = 10
        flame_color = (255, 125, 100)

        pygame.draw.rect(simulation_display, rocket_color, pygame.Rect(rocket_x, rocket_y, rocket_width, rocket_height))
        if simulation.rocket.engines_on and simulation.rocket.fuel_mass > 0:
            pygame.draw.circle(simulation_display, flame_color, (rocket_x + (rocket_width / 2), rocket_y + rocket_height + flame_radius), flame_radius)

def handle_key_press(simulation, key):
    if key == pygame.K_SPACE:
        simulation.rocket.engines_on = not simulation.rocket.engines_on
    elif key == pygame.K_LEFT:
        sys.exit(0)
    elif key == pygame.K_RIGHT:
        sys.exit(0)

if __name__ == "__main__":
    main(sys.argv)