import pygame
import random
from base64 import b64encode
from constants import *
from logger import log_event
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        a_size = (self.radius // ASTEROID_MIN_RADIUS) # asteroid size
        circle_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
                circle_surface,
                pygame.Color(55, 55, 255, 155 // a_size),
                (self.radius, self.radius),
                self.radius,
                LINE_WIDTH * ((a_size*2) - 1) # aka. 1, 3, 5 ....
            )
        draw_pos = (self.position.x - self.radius, self.position.y - self.radius)
        screen.blit(circle_surface, draw_pos)
    def update(self, dt):
        self.position += (self.velocity * dt)
    
    def split(self):
        print(f"=x Asteroid {hex(id(self))[-5:]} hit!") # it's a mess, i know

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
            
