import pygame

from constants import *

M = 28e27 # Mass in kg


class BlackHole:
    def __init__(self,
                 screen: pygame.display,
                 pos: pygame.math.Vector2,
                 velo: pygame.math.Vector2,
                 color: str="red"):
        
        self.screen = screen
        self.pos = pos
        self.velo = velo
        self.color = color

        self.radius = (2 * G * M) / (c ** 2) # Schwarzschild radius
    
    def update(self):
        self.pos += self.velo
    
    def render(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius)


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

    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
        
        screen.fill("black")

        myBlackHole.render()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


