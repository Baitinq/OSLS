import sys
import math
from random import randint

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
    simulation.rocket.current_stage().engines_on = True

    pygame.init()
    pygame.display.set_caption("OSLS - Overly Simple Launch Simulator")
    clock = pygame.time.Clock()

    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 720

    simulation_display = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    paused = False
    while True:
        if not paused:
            draw_simulation(simulation_display, simulation)
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
        if not paused: #tick with pause messes up delta TODO: TODOODODODODODOOD TODO
            print("delta: " + str(delta))
            simulation.tick(delta=delta)

        #TODO: draw body sprite, rocket sprite, clouds sprites, etc.
        #TODO: implement gravity properly (x and y)
        #TODO: do max load on rocket so it blows up
        #TODO: allow multilanguage api for landing algorithms etc

def draw_simulation(simulation_display: type[pygame.Surface], simulation: type[Simulation]) -> None:        
        #draw background
        def linear_gradient(start_color, end_color, length, value_at):
            return [
                int(start_color[j] + (float(value_at)/(length-1))*(end_color[j]-start_color[j]))
                for j in range(3)
            ]

        def get_color_for_height(height: float) -> (int, int, int):
            if height < 70000:
                return linear_gradient((31,118,194), (0, 0, 0), 70000, int(height))
            else:
                return (0, 0, 0)

        #gradient for atmosphere
        simulation_display.fill(get_color_for_height(simulation.rocket_altitude()))

        #draw clouds and stars
        #draw clouds (we need continuity TODO)
        #if simulation.y < 20000 and randint(0, 100) < 5:
        #     pygame.draw.circle(simulation_display, (255, 255, 255), (randint(0, simulation_display.get_width()), randint(0, simulation_display.get_height())), 30)
        #draw stars
        if simulation.rocket_altitude() > 30000:
            for _ in range(100):
                simulation_display.set_at((randint(0, simulation_display.get_width()), randint(0, simulation_display.get_height())), (255, 255, 255))
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

        #draw rocket
        first_stage_height = 90 #TODO
        first_stage_width = 60

        def calculate_rocket_y_based_on_y_speed_accel(display_height: int, rocket_height: int, speed_y: float, accel_y: float) -> int:
            top = display_height / 5 - (rocket_height / 2) #in the case we are accelerating positively
            bottom = display_height - (top * 2)

            return bottom
            
        def calculate_rocket_x_based_on_x_speed_accel(display_width: int, rocket_width: int, speed_x: float, accel_x: float) -> int:
            return display_width / 2 - (rocket_width / 2)

        rocket_x = calculate_rocket_x_based_on_x_speed_accel(simulation_display.get_width(), first_stage_width, None, None)
        rocket_y = calculate_rocket_y_based_on_y_speed_accel(simulation_display.get_height(), first_stage_height, simulation.speed_y, simulation.acceleration_y)

        rocket_color = (244, 67, 54)

        flame_radius = 10
        flame_color = (255, 125, 100)

        #TODO: Rotate rocket with heading
        i = simulation.rocket.stages_spent
        stage_height = first_stage_height / (i + 1)
        stage_y = rocket_y + first_stage_height - stage_height
        for _ in simulation.rocket.stages:
            stage_width = first_stage_width / (i + 1)
            stage_x = rocket_x + i * (stage_width / 2)
            pygame.draw.rect(simulation_display, rocket_color, pygame.Rect(stage_x, stage_y, stage_width, stage_height))
            stage_y -= stage_height / 2
            stage_height /= 2
            i += 1
         
        #draw flame
        if simulation.rocket.current_stage().engines_on and simulation.rocket.current_stage().fuel_mass > 0:
            pygame.draw.circle(simulation_display, flame_color, (rocket_x + (first_stage_width / 2), rocket_y + first_stage_height + flame_radius), flame_radius)

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
