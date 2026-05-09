import pygame
from constants import *

class UI:
    def __init__(self, screen):
        self.font = pygame.font.Font("fonts/Square.ttf", 24)
        self.screen = screen
        self.score = 0
    def update(self, type, value):
        if type == "score":
            self.score += value
    def draw(self):
        score_label = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_label, (10, 10))
