import pygame
import random
from MODULES.constants import *
from MODULES.logger import log_event
from MODULES.circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(
                screen,
                "white",
                self.position,
                self.radius,
                LINE_WIDTH
            )
    def update(self, dt):
        self.position += (self.velocity * dt)
    
    def split(self):
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.kill()
            return
        else:
            log_event("asteroid_split")

            # % set values and kill the parent
            angle = random.uniform(20, 50)
            velocity = self.velocity.copy()
            position = self.position.copy()
            self.kill()
            
            # % calculate vectors and radius for both child asteroids

            c_asteroid_vec1, c_asteroid_vec2 = ( # child asteroids vectors
                    velocity.rotate(angle),
                    velocity.rotate(-angle))

            c_asteroid_r = self.radius - ASTEROID_MIN_RADIUS # child asteroids radiuses
            
            # % initialize child asteroids
            child_asteroid_1, child_asteroid_2 = (
                    Asteroid(position.x, position.y, c_asteroid_r),
                    Asteroid(position.x, position.y, c_asteroid_r))

            child_asteroid_1.velocity = c_asteroid_vec1
            child_asteroid_2.velocity = c_asteroid_vec2

            
