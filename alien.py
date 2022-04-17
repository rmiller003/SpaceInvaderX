import pygame


class Alien(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        self.image = pygame.image.load('xship2.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (x,y))

        if color == 'xship2.png': self.value = 100

    def update(self,direction):
        self.rect.x += direction

class Extra(pygame.sprite.Sprite):
    def __init__(self,side,screen_width):
        super().__init__()
        self.image = pygame.image.load('xship1.png').convert_alpha()

        if side == 'right':
            x = screen_width + 50
            self.speed = -3
        else:
            x = -50
            self.speed = 3

        self.rect = self.image.get_rect(topleft = (x,80))

    def update(self):
            self.rect.x += self.speed

class Extra2(pygame.sprite.Sprite):
    def __init__(self,side,screen_width):
        super().__init__()
        self.image = pygame.image.load('xship3.png').convert_alpha()

        if side == 'left':
            x = screen_width + -50
            self.speed = -4
        else:
            x = 50
            self.speed = 4

        self.rect = self.image.get_rect(topright = (x,90))

    def update(self):
        self.rect.x += self.speed