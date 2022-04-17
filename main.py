# This is a clone of the classic Space Invader game codded in Python 3.9 using the pygame module

import pygame, sys
from player import Player
import obstacle
from alien import Alien, Extra, Extra2
from random import choice, randint
from laser import Laser

class Game:
    def __init__(self):
        # Player setup
        player_sprite = Player((screen_width / 2,screen_height),screen_width,5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # health and score setup
        self.lives = 3
        self.live_surf = pygame.image.load('player.png').convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surf.get_size()[0] * 2 +20)
        self.score = 0
        self.font = pygame.font.Font('Pixeled.ttf', 20)

        # Obstacle setup
        self.shape = obstacle.shape
        self.block_size = 6
        self.blocks =pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_position = [num * (screen_width / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_position, x_start = screen_width / 15, y_start= 480)

        # Alien setup
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 7)
        self.alien_direction = 1

        # Extra setup
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40,80)

        self.extra2 = pygame.sprite.GroupSingle()
        self.extra2_spawn_time = randint(40,80)

        # Audio Setup
        music = pygame.mixer.Sound('music.wav')
        music.set_volume(0.2)
        music.play(loops = -1)


    def create_obstacles(self, x_start, y_start,offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index,col in enumerate(row):
                if col == 'x':
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = obstacle.Block(self.block_size,(241,79,80),x,y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self,*offset,x_start,y_start):
        for offset_x in offset:
            self.create_obstacles(x_start,y_start,offset_x)


    def alien_setup(self,rows,cols,x_distance = 72,y_distance = 48,x_offset = 70, y_offset = 50):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset

                if row_index == 0: alien_sprite = Alien('yellow',x,y)
                elif 1 <= row_index <= 2: alien_sprite = Alien('green',x,y)
                else: alien_sprite = Alien('red',x,y)
                self.aliens.add(alien_sprite)

    def alien_position_checker(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= screen_width:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <=0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self,distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center,6,screen_height)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_timer(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(['right', 'left']),screen_width))
            self.extra_spawn_time = randint(400,800)

    def extra2_alien_timer(self):
        self.extra2_spawn_time -= 1
        if self.extra2_spawn_time <= 0:
            self.extra2.add(Extra2(choice(['left', 'right']),screen_width))
            self.extra2_spawn_time = randint(400,800)

    def collision_checks(self):

       #player lasers
       if self.player.sprite.lasers:
           for laser in self.player.sprite.lasers:

               # obstacle collisions
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                # Alien collisions
                if pygame.sprite.spritecollide(laser,self.aliens,True):
                    self.score += 100
                    laser.kill()


                # Extra ship collision
                if pygame.sprite.spritecollide(laser,self.extra,True):
                    self.score += 500
                    laser.kill()

                if pygame.sprite.spritecollide(laser,self.extra2,True):
                    self.score += 300
                    laser.kill()

        # Alien laser
       if self.alien_lasers:
            for laser in self.alien_lasers:
                # obstacle collisions
                if pygame.sprite.spritecollide(laser,self.blocks,True):
                    laser.kill()

                if pygame.sprite.spritecollide(laser,self.player,False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()

      # Aliens
       if self.aliens:
           for alien in self.aliens:
               pygame.sprite.spritecollide(alien,self.blocks,True)

               if pygame.sprite.spritecollide(alien,self.player,False):
                   pygame.quit()
                   sys.exit()

    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surf.get_size()[0] + 10))
            screen.blit(self.live_surf,(x,8))

    def display_score(self):
        score_surf = self.font.render(f'score: {self.score}',False, 'white')
        score_rect = score_surf.get_rect(topleft = (10,-10))
        screen.blit(score_surf, score_rect)

    def run(self):
        self.player.update()
        self.alien_lasers.update()
        self.extra.update()
        self.extra2.update()

        self.aliens.update(self.alien_direction)
        self.alien_position_checker()
        self.extra_alien_timer()
        self.extra2_alien_timer()
        self.collision_checks()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)
        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.extra2.draw(screen)
        self.display_lives()
        self.display_score()

if __name__ == '__main__':
    pygame.init()
    screen_width = 650
    screen_height = 650
    screen = pygame.display.set_mode((screen_width, screen_height))
    background_image = pygame.image.load('bg.png')
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER,800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()


        screen.fill((30,30,30))
        screen.blit(background_image, (0,0))
        game.run()

        pygame.display.flip()

        clock.tick(60)
