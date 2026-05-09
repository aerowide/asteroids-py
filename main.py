import pygame
import sys
from logger import log_state, log_event
from constants import *
from ui import UI
from PLAYER.player import Player
from PLAYER.shot import Shot
from ASTEROIDS.asteroid import Asteroid
from ASTEROIDS.asteroidfield import AsteroidField

def main():
    # --- initialize pygame
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    dt = 0
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    
    # --- set screen size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    canvas = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))

    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

    # --- init UI
    ui = UI(canvas)
    bg_gradient = pygame.image.load("bg/gradient.png").convert()
     
    # -- groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    # -- init player and it's bullets
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    
    player = Player(GAME_WIDTH//2, GAME_HEIGHT//2)
    
    # -- init asteroids
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid_field = AsteroidField()

    # --- game loop
    while True:
        # - logs
        log_state()

        # - events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return;

        # - delta time
        dt = clock.tick(60) / 1000

        # - render
        canvas.blit(pygame.transform.scale(bg_gradient, (GAME_WIDTH, GAME_HEIGHT)), (0, 0))
        ui.draw()
        for item in drawable:
            item.draw(canvas) 
        updatable.update(dt)
        scaled_canvas = pygame.transform.scale(canvas, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(scaled_canvas, (0, 0))

        # - check for collision
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")

                print("\n")
                print(" Game over! ".center(25, "x"))
                print(f" Score: {ui.score} ".center(25, "x"))
                print("\n")

                sys.exit()
            for bullet in shots:
                if asteroid.collides_with(bullet):
                    ui.update("score", 4 - (asteroid.radius // ASTEROID_MIN_RADIUS))
                    log_event("asteroid_shot")
                    bullet.kill()
                    asteroid.split(clock, dt)


        pygame.display.flip()
        

if __name__ == "__main__":
    main()
