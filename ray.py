import math

import pygame

from black_hole import BlackHole
from constants import *


class Ray:
    def __init__(self,
                 screen: pygame.display,
                 pos_real: pygame.math.Vector2,
                 velo: pygame.math.Vector2,
                 black_hole: BlackHole,
                 color: str="white"):
        
        self.screen = screen
        self.black_hole = black_hole
        self.color = color

        self.active = True
        
        self.WIDTH, self.HEIGHT = pygame.display.get_surface().get_size()

        self.pos_adjusted = pos_real - black_hole.pos
        self.pos_adjusted.y = -self.pos_adjusted.y
        self.r = math.hypot(self.pos_adjusted.x, self.pos_adjusted.y)
        self.phi = math.atan2(self.pos_adjusted.y, self.pos_adjusted.x)

        # self.dr = math.hypot(velo.x, velo.y)
        # self.dphi = math.atan2(velo.y, velo.x)

        self.velo = velo # TODO Get velocity in polar coordinates working

        self.r_s = self.black_hole.radius
    
    def update_cartesian(self):
        self.pos_adjusted += self.velo

        self.r = math.hypot(self.pos_adjusted.x, self.pos_adjusted.y)
        self.phi = math.atan2(self.pos_adjusted.y, self.pos_adjusted.x)

        if self.r <= self.r_s:
            self.active = False

    def update_polar(self):
        if self.r <= self.r_s:
            self.active = False

    def render(self):
        self.pos_adjusted = pygame.math.Vector2(self.r * math.cos(self.phi),
                                                self.r * math.sin(self.phi))
        pos_real = self.pos_adjusted + self.black_hole.pos
        pos_real.y = self.HEIGHT - pos_real.y
        
        if self.active:
            pygame.draw.circle(self.screen, self.color, pos_real, 1)
        
        # TODO Add trail function for gradiant light trail


if __name__ == "__main__":
    loop = True
    
    pygame.init()
    WIDTH = 800
    HEIGHT = 600
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    myBlackHole = BlackHole(screen,
                            pygame.math.Vector2(400, 300),
                            pygame.math.Vector2(0, 0))

    myRay = Ray(screen,
                pygame.math.Vector2(100, 300),
                pygame.math.Vector2(5, 0),
                myBlackHole)

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
        
        screen.fill("black")
        
        myRay.update_cartesian()

        myBlackHole.render()
        myRay.render()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
