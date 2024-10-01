#project was made with files from Clear code
#https://github.com/clear-code-projects/5games

import pygame
from Tools.scripts.dutree import display
from sympy.core.random import randint
from random import randint
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self):
        super().__init__()# for inheretance to init parent class
        self.surf = pygame.image.load('source_files/images/player.png')
        self.rect = self.surf.get_rect(center = (window_width/2,window_height-100))
        self.speed = 500
        self.direction = pygame.math.Vector2()

    def update(self):
        keys = pygame.key.get_pressed()
        self.direction.x = (int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]))  # x speed is faster
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])  # y speed
        if (self.rect.bottom > window_height and self.direction.y > 0) or (
                self.rect.top < 0 and self.direction.y < 0):
            self.direction.y = 0
        if (self.rect.right > window_width and self.direction.x > 0) or (
                self.rect.left < 0 and self.direction.x < 0):
            self.direction.x = 0
        if self.direction:
            self.direction = self.direction.normalize()  # normalize to keep speed in diagonal movment same
        self.rect.center += self.direction * self.speed * dt


#general setup
#pygame.init()# init pygame, causes freeze at start - neet to see if something goes wrong
window_width,window_height = 1280, 720 #screen size
screen = pygame.display.set_mode((window_width,window_height))# create screen
pygame.display.set_caption('Space Shooter')
running = True
clock =pygame.time.Clock()  # control framerate, control
FPS_target = 99
# create  player and items

player = Player()

laser_surf = pygame.image.load('source_files/images/laser.png')
laser_rect = laser_surf.get_rect(center = (20,window_height-40))

meteor_surf = pygame.image.load('source_files/images/meteor.png')
meteor_rect = meteor_surf.get_rect(center = (window_width/2,window_height/2))

star_surf = pygame.image.load('source_files/images/star.png')
star_pos= [(randint(0,window_width),randint(0,window_height)) for i in range(20)]

# game loop
while running:
    dt = clock.tick(FPS_target) /1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:# single time use- so key press will register just once
            if event.key == pygame.K_SPACE:# fire lasr - need to implement
                print("fire")
    #player update
    player.update()
    #draw game
    screen.fill('azure3')#fill with blue color
    for pos in star_pos :
        screen.blit(star_surf,pos)

    screen.blit(player.surf,player.rect)
    screen.blit(laser_surf,laser_rect)
    screen.blit(meteor_surf,meteor_rect)
    pygame.display.update()# or flip - flip updates a part of the window , update the whole window

pygame.quit()
