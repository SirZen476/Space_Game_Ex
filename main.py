#project was made with files from Clear code
#https://github.com/clear-code-projects/5games

import pygame
from Tools.scripts.dutree import display
from sympy.core.random import randint
from random import randint
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, groups):
        super().__init__(groups)# for inheretance to init parent class
        self.image = pygame.image.load('source_files/images/player.png')
        self.rect = self.image.get_rect(center = (window_width/2,window_height-100))
        self.speed = 500
        self.direction = pygame.math.Vector2()

    def update(self,dt):
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

class Star(Sprite):
    def __init__(self,groups,image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(center = (randint(0,window_width),randint(0,window_height)))


class Laser(Sprite):
    def __init__(self,groups ,x,y):
        super().__init__(groups)
        self.image = pygame.image.load('source_files/images/laser.png')
        self.rect = self.image.get_rect(center = (x,y-20))
        self.speed = 0# when moving 800
        self.direction = pygame.math.Vector2(0,-1)# goes up only
    def fire(self):
        self.speed = 700
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt

class Meteor(Sprite):
    def __init__(self,groups,x,y,image ):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(center = (x,y))
        self.speed = 300
        self.direction = pygame.math.Vector2(0,1)
        self.hp = 5
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt





#general setup
#pygame.init()# init pygame, causes freeze at start - neet to see if something goes wrong
window_width,window_height = 1280, 720 #screen size
screen = pygame.display.set_mode((window_width,window_height))# create screen
pygame.display.set_caption('Space Shooter')
running = True
clock =pygame.time.Clock()  # control framerate, control
FPS_target = 99
# create  Group
all_sprites = pygame.sprite.Group()
# add items to game
laser = Laser(all_sprites,20,window_height-20)
image_star = pygame.image.load('source_files/images/star.png')# load before so we wont have to load 20 times the same image
for i in range(20):
    star = Star(all_sprites,image_star)
image_meteor = pygame.image.load('source_files/images/meteor.png')
meteor = Meteor(all_sprites,window_width/2,window_height/2, image_meteor)
player = Player(all_sprites)



# game loop
while running:
    dt = clock.tick(FPS_target) /1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # fire laser - just one press
            laser_fire = Laser(all_sprites,player.rect.centerx,player.rect.centery)
            laser_fire.fire()

    #update
    all_sprites.update(dt)
    #draw game

    screen.fill('black')#fill with blue color
    all_sprites.draw(screen)
    pygame.display.update()# or flip - flip updates a part of the window , update the whole window



pygame.quit()
