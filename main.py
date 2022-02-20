# This is a clone of the classic Space Invader game codded in Python 3.9 using the pygame module

import pygame, sys

class Game:
    def __init__(self):
        pass

    def run(self):
        pass
        # update all sprite groups
        # draw all sprite groups

if __name__ == '__main__':
    pygame.init()
    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width,screen_height))
    clock = pygame.time.Clock()
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30.30.30))
        game.run()

        pygame.display.flip()
        clock.tick(60)



