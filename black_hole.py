import pygame

class BlackHole:
    def __init__(self, screen, location, mass):
        self.screen = screen

        self.x = location[0]
        self.y = location[1]

        M = 28e27
        G = 6.67430e-11
        c = 299792458

        self.r = (2 * G * M) / (c ** 2)

        pygame.draw.circle(self.screen, "red", (400, 300), self.r)
    
    def update(self):
        pygame.draw.circle(self.screen, "red", (self.x, self.y), self.r)
