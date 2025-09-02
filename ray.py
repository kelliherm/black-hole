import math
import pygame

class Ray:
    def __init__(self, screen, location, velocity, black_hole):
        self.screen = screen

        self.black_hole = black_hole

        self.alive = True

        self.positions = []
        
        self.x = location[0]
        self.y = location[1]
        self.dx = velocity[0]
        self.dy = velocity[1]

        #pygame.draw.circle(self.screen, "white", (self.x, self.y), 1)
    
    def update(self):
        x, y = self.black_hole.x - self.x, self.black_hole.y  - self.y
        self.r = math.sqrt(x ** 2 + y ** 2)
        try:
            self.theta = math.atan(y / x)
        except:
            pass

        if self.black_hole.r >= self.r:
            self.alive = False
        
        self.positions.insert(0, (self.x, self.y))

        for index in range(len(self.positions)):
            if self.alive == True:
                pygame.draw.circle(self.screen, "white", (self.positions[index][0], self.positions[index][1]), 1)
            else:
                self.dx = 0
                self.dy = 0

        max_trail = 50
        if len(self.positions) > max_trail:
            self.positions.pop(max_trail)

        self.x += self.dx
        self.y += self.dy
