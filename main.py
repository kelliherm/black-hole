import math
import random
import sys

import pygame

from ray import Ray
from constants import *


def circular_speed(r, M, r_s):
    """Returns the circular speed using Paczynski-Wiita potential"""
    denom = (r - r_s)
    if denom <= 0:
        return 0.0
    v2 = r * G * M / (denom * denom)
    return math.sqrt(max(0.0, v2))

def schwarzschild_radius(M):
    """Returns the Schwarzchild radius of a black hole given a certain mass"""
    return 2.0 * G * M / (c * c)

def spawn_disk(n=N_RAYS, inner=DISK_INNER, outer=DISK_OUTER, M=BH_MASS):
    """Creates many rays"""
    r_s = schwarzschild_radius(M)
    parts = []
    for i in range(n):
        # sample radius (prefer more rays near inner edge): use sqrt distribution
        u = random.random()
        r = math.sqrt(u * (outer*outer - inner*inner) + inner*inner)
        theta = random.random() * 2 * math.pi
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        # circular speed + small random eccentricity
        v = circular_speed(r, M, r_s)
        # direction orthogonal to radius (counter-clockwise)
        vx = -v * math.sin(theta)
        vy = v * math.cos(theta)
        # small random perturbation
        vx *= (1.0 + (random.random()-0.5)*0.02)
        vy *= (1.0 + (random.random()-0.5)*0.02)
        p = Ray(x, y, vx, vy)
        parts.append(p)
    return parts

def temp_color(r, r_min, r_max):
    # normalized t: 1 at inner, 0 at outer
    t = max(0.0, min(1.0, (r_max - r) / (r_max - r_min)))
    # interpolate between red (outer) and white (inner)
    # simple mapping
    rcol = int(200 + 55 * t)
    gcol = int(40 + 200 * t)
    bcol = int(10 + 200 * t * t)
    return (min(255, rcol), min(255, gcol), min(255, bcol))

def convert_to_screen(x, y, origin_x, origin_y, scale):
    """Convert the simulation coordinates to Pygame screen coordinates"""
    sx = int(origin_x + x * scale)
    sy = int(origin_y - y * scale)
    return sx, sy

def draw_text(surf, text, x, y, col=(255,255,255)):
    img = font.render(text, True, col)
    surf.blit(img, (x,y))

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 20)
    pygame.display.set_caption("Black Hole Simulation")

    origin_x, origin_y = WIDTH // 2, HEIGHT // 2

    scale = 40.0  # pixels per simulation unit
    BH_M = BH_MASS
    BH_M = 1.0
    r_s = schwarzschild_radius(BH_M)

    particles = spawn_disk()

    show_trails = True

    running = True
    paused = False

    while running:
        dt = 1.0 / FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    particles = spawn_disk()
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    BH_M *= 1.2
                    r_s = schwarzschild_radius(BH_M)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                    BH_M /= 1.2
                    r_s = schwarzschild_radius(BH_M)
                elif event.key == pygame.K_UP:
                    scale *= 1.1
                elif event.key == pygame.K_DOWN:
                    scale /= 1.1
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    sx = (mx - origin_x)/scale
                    sy = (origin_y - my)/scale
                    r = math.hypot(sx, sy)
                    theta = math.atan2(sy, sx)
                    v = circular_speed(r, BH_M, r_s)
                    v *= 1.2
                    vx = -v * math.sin(theta)
                    vy = v * math.cos(theta)
                    particles.append(Ray(sx, sy, vx, vy))
        
        if not paused:
            # step physics (we can substep for stability)
            substeps = 2
            subdt = dt / substeps
            for _ in range(substeps):
                # update all particles
                alive = []
                for p in particles:
                    p.step(subdt, BH_M, r_s)
                    # detect "swallowed" by horizon (r <= r_s*1.02) -> drop particle
                    r_now = math.hypot(p.x, p.y)
                    if r_now > r_s * 1.02 and r_now < 1e6:
                        alive.append(p)
                    # else: particle swallowed, skip
                particles = alive
        
        screen.fill((8, 8, 15))
        # draw horizon (filled)
        horizon_px = max(1, int(r_s * scale))
        pygame.draw.circle(screen, (10,10,10), (origin_x, origin_y), horizon_px)
        # light ring (photon-ish) approximate: draw faint ring at ~1.5*r_s
        photon_ring_px = int(r_s * 1.5 * scale)
        if photon_ring_px > 2:
            pygame.draw.circle(screen, (80,80,100), (origin_x, origin_y), photon_ring_px, 1)

        draw_text(screen, f"Particles: {len(particles)}", 8, 8)
        draw_text(screen, f"BH mass: {BH_M:.1f}    r_s: {r_s:.3f} simunits    ({horizon_px}px)", 8, 28)
        draw_text(screen, "Controls: Space = reset rays    LeftClick = spawn ray    +/- mass", 8, 52)
        draw_text(screen, "P pause   Esc quit", 8, 72)

        # draw particles
        for p in particles:
            r = math.hypot(p.x, p.y)
            cx = temp_color(r, DISK_INNER, DISK_OUTER)
            sx, sy = convert_to_screen(p.x, p.y, origin_x, origin_y, scale)
            if show_trails and len(p.trail) >= 2:
                pts = [convert_to_screen(xx, yy, origin_x, origin_y, scale) for (xx, yy) in p.trail]
                # Draw fading trail
                for i in range(len(pts)-1):
                    alpha = int(255 * (1 - i/len(pts)))
                    col = (max(0, cx[0]-i*3), max(0, cx[1]-i*2), max(0, cx[2]-i))
                    pygame.draw.line(screen, col, pts[i], pts[i+1], 1)
            pygame.draw.circle(screen, cx, (sx, sy), RAY_SIZE)
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()
