import pygame

from constants import *

M = 28e27 # Mass in kg

class BlackHole:
    def __init__(self,
                 screen,
                 pos: pygame.math.Vector2,
                 velo: pygame.math.Vector2,
                 color: str="red"):
        
        self.screen = screen
        self.pos = pos
        self.velo = velo
        self.color = color

        self.radius = (2 * G * M) / (c ** 2) # Schwarzschild radius
    
    def update(self):
        self.pos = self.pos + self.velo
    
    def render(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius)
