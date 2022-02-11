import pygame
from pygame.locals import *

from simulation import Simulation
from rocket import Rocket

class Sprite_Rocket(pygame.sprite.Sprite):
    def __init__(self, simulation: type[Simulation], floor: int):
        super().__init__()
        self.simulation = simulation
        self.rocket = self.simulation.rocket
        self.floor = floor

    def update(self, display_width, display_height):
        first_stage_height = 90 #TODO
        first_stage_width = 60
        rocket_color = (244, 67, 54)

        flame_radius = 10
        flame_color = (255, 125, 100)

        total_rocket_height = flame_radius * 2
        i = self.simulation.rocket.stages_spent
        stage_height = first_stage_height / (i + 1)
        for _ in self.simulation.rocket.stages:
            total_rocket_height += stage_height
            stage_height /= 2
            i += 1
        
        self.image = pygame.Surface([first_stage_width, total_rocket_height], pygame.SRCALPHA)
        #self.image.fill((0, 255, 0))
        
        i = self.simulation.rocket.stages_spent
        stage_height = first_stage_height
        stage_y = first_stage_height
        for _ in self.simulation.rocket.stages:
            stage_width = first_stage_width / (i + 1)
            stage_x = i * (stage_width / 2)
            
            pygame.draw.rect(self.image, rocket_color, pygame.Rect(stage_x, total_rocket_height - stage_y - (flame_radius * 2), stage_width, stage_height))

            stage_y += stage_height / 2
            stage_height /= 2

            i += 1

        #draw flame: TODO: Flame should show direction somehow (gimbal)
        if self.simulation.rocket.current_stage().engines_on and self.simulation.rocket.current_stage().fuel_mass > 0:
            pygame.draw.circle(self.image, flame_color, (first_stage_width / 2, total_rocket_height - flame_radius), flame_radius)
        

        
        #heading
        self.image = pygame.transform.rotozoom(self.image, -self.simulation.heading, 1)

        self.rect = self.image.get_rect()

        rocket_x = display_width / 2 - (first_stage_width / 2)
        rocket_y = display_height - self.floor#TODO: 100 is a const. SHARE THAT ACROSS THIGNS (FLOOR)

        self.rect.bottomleft = [rocket_x, rocket_y]

    