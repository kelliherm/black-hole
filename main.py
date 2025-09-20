import pygame

from black_hole import BlackHole
from ray import Ray


pygame.init()
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

running = True
paused = False

black_hole = BlackHole(screen,
                       pygame.math.Vector2(WIDTH / 2, HEIGHT / 2),
                       pygame.math.Vector2(0, 0),)

n = 10
rays = [Ray(screen,
            pygame.math.Vector2(0, (HEIGHT / (2 * n)) + i * (HEIGHT / n)),
            pygame.math.Vector2(1, 0),
            black_hole)
            for i in range(n)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    screen.fill("black")

    black_hole.update()

    for ray in rays:
        ray.update_cartesian()

    black_hole.render()
    for ray in rays:
        ray.render()

    pygame.display.flip()
    clock.tick(300)

pygame.quit()
