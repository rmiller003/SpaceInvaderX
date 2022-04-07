import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        file_path = '../graphics/' + color + '.png'
        self.image = pygame.image.load('red.png').convert_alpha()
        #self.image = pygame.image.load('green.png').convert_alpha()
        #self.image = pygame.image.load('yellow.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))
