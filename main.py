import pygame
from logger import log_state
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from player import Player

def main():
    # initialize pygame
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    
    # set screen size
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    print(f"Screen width: {SCREEN_WIDTH}\nScreen height: {SCREEN_HEIGHT}")

    player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    
    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return;

        screen.fill("black")
        player.draw(screen)
        dt = clock.tick(60) / 1000
        player.update(dt)
        pygame.display.flip()
        

if __name__ == "__main__":
    main()
