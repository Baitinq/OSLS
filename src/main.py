import sys
import math

from engine import Engine
from fuel import Fuel
from stage import Stage
from rocket import Rocket
from atmosphere import Atmosphere
from body import Body
from universe import Universe
from simulation import Simulation

import pygame
from pygame.locals import *

from gui.background_sprite import Sprite_Background
from gui.rocket_sprite import Sprite_Rocket
from gui.body_sprite import Sprite_Body

def main(argv):
    raptor_engine = Engine(name="raptor", isp=360, max_flow_rate=931) #https://en.wikipedia.org/wiki/SpaceX_Raptor
    methane_fuel = Fuel(name="methane") #TODO: more

    #https://en.wikipedia.org/wiki/SpaceX_Starship
    first_stage = Stage(name="superheavy booster",
                        stage_mass=180000,
                        engine=raptor_engine,
                        engine_number=33,
                        max_engine_gimbaling_angle=30,
                        fuel_type=methane_fuel,
                        fuel_mass=3600000,
                        x_drag_coefficient=1.16,#https://www.sciencedirect.com/science/article/abs/pii/S002980181400167X
                        x_cross_sectional_area=(69 * 9), #booster height: 69m, diameter:9m
                        y_drag_coefficient=1.28,#https://www.grc.nasa.gov/www/k-12/rocket/shaped.html
                        y_cross_sectional_area=(math.pi * (4.5**2)) #booster radius: 4.5m
                        )

    second_stage = Stage(name="starship",
                        stage_mass=80000,
                        engine=raptor_engine,
                        engine_number=6,
                        max_engine_gimbaling_angle=30,
                        fuel_type=methane_fuel,
                        fuel_mass=1200000,
                        x_drag_coefficient=1.16,#https://www.sciencedirect.com/science/article/abs/pii/S002980181400167X
                        x_cross_sectional_area=(49 * 9), #rocket height: 49m, diameter:9m
                        y_drag_coefficient=0.8,#https://www.grc.nasa.gov/www/k-12/rocket/shaped.html
                        y_cross_sectional_area=(math.pi * (4.5**2))#rocket radius: 4.5m
                        )

    rocket = Rocket(name="starship launch system", 
                    stages=[first_stage, second_stage],
                    payload_mass=100
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
                        G=6.67E-11
                        )
    
    simulation = Simulation(universe, body, rocket)

    pygame.init()
    pygame.display.set_caption("OSLS - Overly Simple Launch Simulator")
    clock = pygame.time.Clock()

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 720

    sprite_group = pygame.sprite.Group()

    #cloud_sprite = Sprite_Cloud(simulation) #TODO

    floor = 100 #100px is the floor of the drawing (where the rocket stops and where the body surface is)

    sprite_group.add(Sprite_Background(simulation),
                     Sprite_Body(simulation, floor), 
                     Sprite_Rocket(simulation, floor))

    simulation_display = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    paused = False
    while True:
        if not paused:
            sprite_group.update(simulation_display.get_width(), simulation_display.get_height())
            sprite_group.draw(simulation_display)
            draw_text_info(simulation_display, simulation)
            pygame.display.update()

        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:  
                pygame.quit()  
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit()
                elif event.key == pygame.K_SPACE:
                    paused = not paused
                else:
                    handle_key_press(simulation, event.key)

        delta = clock.tick(60) / 1000 #60fps #are we using delta in the simulation tick everywhere needed?
        if not paused:
            print("delta: " + str(delta))
            simulation.tick(delta=delta)

        #TODO: implement gravity properly (x and y)
        #TODO: implement apoapsis and periapsis calculation
        #TODO: draw good rocket sprite, persistant clouds and star sprites, etc.
        #TODO: do actual aerodynamic load so heading depends on that and not on speed
        #TODO: do max load on rocket so it blows up
        #TODO: allow multilanguage api for landing algorithms etc

def draw_text_info(simulation_display: type[pygame.Surface], simulation: type[Simulation]) -> None:        
        #draw stats text
        font = pygame.font.SysFont("Comic Sans MS", 30)

        g = simulation.body.g(simulation.universe.G, simulation.rocket_altitude())
        curr_thrust = simulation.rocket.current_stage().current_thrust(g, simulation.heading)

        simulation_display.blit(font.render("Simulation time: {:.0f}s".format(simulation.time), False, (255, 255, 255)),(0,0))
        simulation_display.blit(font.render("Altitude: {:.0f}m".format(simulation.rocket_altitude()), False, (255, 255, 255)),(0,40))
        simulation_display.blit(font.render("X: {:.0f}m".format(simulation.x), False, (255, 255, 255)),(0,80))
        simulation_display.blit(font.render("Y: {:.0f}m".format(simulation.y), False, (255, 255, 255)),(0,120))
        simulation_display.blit(font.render("Speed x: {:.0f}m/s".format(simulation.speed_x), False, (255, 255, 255)),(0,160))
        simulation_display.blit(font.render("Speed y: {:.0f}m/s".format(simulation.speed_y), False, (255, 255, 255)),(0,200))
        simulation_display.blit(font.render("Acceleration x: {:.2f}m/s2".format(simulation.acceleration_x), False, (255, 255, 255)),(0,240))
        simulation_display.blit(font.render("Acceleration y: {:.2f}m/s2".format(simulation.acceleration_y), False, (255, 255, 255)),(0,280))
        simulation_display.blit(font.render("Thrust x: {:.0f}N".format(simulation.rocket.current_stage().current_thrust(g, simulation.heading)[0]), False, (255, 255, 255)),(0,320))
        simulation_display.blit(font.render("Thrust y: {:.0f}N".format(simulation.rocket.current_stage().current_thrust(g, simulation.heading)[1]), False, (255, 255, 255)),(0,360))
        simulation_display.blit(font.render("Fuel in stage: {:.0f}kg".format(simulation.rocket.current_stage().fuel_mass), False, (255, 255, 255)),(0,400))
        simulation_display.blit(font.render("Stage mass: {:.0f}kg".format(simulation.rocket.current_stage().total_mass()), False, (255, 255, 255)),(0,440))
        simulation_display.blit(font.render("Rocket mass: {:.0f}kg".format(simulation.rocket.total_mass()), False, (255, 255, 255)),(0,480))
        simulation_display.blit(font.render("Stage number: {:.0f}".format(simulation.rocket.stages_spent), False, (255, 255, 255)),(0,520))
        simulation_display.blit(font.render("Throttle: {:.0f}%".format(simulation.rocket.current_stage().throttle), False, (255, 255, 255)),(0,560))
        simulation_display.blit(font.render("Gimbal: {:.2f}deg".format(simulation.rocket.current_stage().gimbal), False, (255, 255, 255)),(0,600))
        simulation_display.blit(font.render("Heading: {:.2f}deg".format(simulation.heading), False, (255, 255, 255)),(0,640))

def handle_key_press(simulation, key):
    if key == pygame.K_x:
        simulation.rocket.current_stage().engines_on = not simulation.rocket.current_stage().engines_on
    elif key == pygame.K_z:
        simulation.rocket.perform_stage_separation(True)
    elif key == pygame.K_DOWN:
        current_stage = simulation.rocket.current_stage()
        if current_stage.throttle > 0:
            current_stage.throttle -= 1
    elif key == pygame.K_UP:
        current_stage = simulation.rocket.current_stage()
        if current_stage.throttle < 100:
            current_stage.throttle += 1
    elif key == pygame.K_LEFT:
        current_stage = simulation.rocket.current_stage()
        if current_stage.gimbal > 0 - current_stage.max_engine_gimbaling_angle:
            current_stage.gimbal -= 1
    elif key == pygame.K_RIGHT:
        current_stage = simulation.rocket.current_stage()
        if current_stage.gimbal < 0 + current_stage.max_engine_gimbaling_angle:
            current_stage.gimbal += 1

if __name__ == "__main__":
    main(sys.argv)
