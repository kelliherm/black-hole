import pygame

from black_hole import BlackHole
from ray import Ray

pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))

clock = pygame.time.Clock()

sim_over = False

black_hole = BlackHole(screen, (400, 300), 100)

n = 10
rays = [Ray(screen, (0, (height / (2 * n)) + i * (height / n)), (1, 0), black_hole) for i in range(n)]

while not sim_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sim_over = True

    # RENDER YOUR GAME HERE

    screen.fill("black")

    black_hole.update()

    for ray in rays:
        ray.update()


    pygame.display.flip()

    clock.tick(300)

pygame.quit()
