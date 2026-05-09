import pygame
import random
from base64 import b64encode
from constants import *
from logger import log_event
from circleshape import CircleShape

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.exploding = False
        self.explode_timer = 0


    def draw(self, screen):
        a_size = (self.radius // ASTEROID_MIN_RADIUS) # asteroid size
        circle_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        
        draw_width = 0 if self.exploding else LINE_WIDTH * a_size
        
        pygame.draw.circle(
                circle_surface,
                pygame.Color(55, 55, 255, 155 // a_size),
                (self.radius, self.radius),
                self.radius,
                draw_width
            )
        draw_pos = (self.position.x - self.radius, self.position.y - self.radius)
        screen.blit(circle_surface, draw_pos)
    def update(self, dt):
        if self.exploding:
            self.explosion_timer -= dt
            if self.explosion_timer <= 0: self.kill()
            return
        self.position += (self.velocity * dt)
    
    def split(self, clock, dt):
        print(f"=x Asteroid {hex(id(self))[-5:]} hit!") # it's a mess, i know

        if not self.exploding:
            self.exploding = True
            self.explosion_timer = 0.11

        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")

            # % set values and kill the parent
            angle = random.uniform(20, 50)
            velocity = self.velocity.copy()
            position = self.position.copy()
            
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
            
