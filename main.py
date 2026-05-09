import pygame
import sys
from logger import log_state, log_event
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from PLAYER.player import Player
from PLAYER.shot import Shot
from ASTEROIDS.asteroid import Asteroid
from ASTEROIDS.asteroidfield import AsteroidField

def main():
    # --- initialize pygame
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    
    # --- set screen size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")
     
    # -- groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    # -- init player and it's bullets
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    
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
        screen.fill("black")
        for item in drawable:
            item.draw(screen) 
        updatable.update(dt)

        # - check for collision
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
            for bullet in shots:
                if asteroid.collides_with(bullet):
                    log_event("asteroid_shot")
                    bullet.kill()
                    asteroid.split()

        pygame.display.flip()
        

if __name__ == "__main__":
    main()
