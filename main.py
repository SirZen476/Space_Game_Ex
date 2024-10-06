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
        self.can_shoot = True
        self.last_shot = 0.0
        self.cooldown = 400

    def update(self,dt):
        current_shot = pygame.time.get_ticks()
        if current_shot - self.last_shot > self.cooldown:
            self.can_shoot = True
        keys = pygame.key.get_pressed()
        #chek for shot and fire
        if(keys[pygame.K_SPACE] and self.can_shoot):
            laser_fire = Laser(all_sprites, self.rect.centerx, self.rect.centery, image_laser)  # add new laser
            laser_fire.fire()
            self.last_shot = pygame.time.get_ticks()
            self.can_shoot = False
        #movment
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
    def __init__(self,groups ,x,y,image):
        super().__init__(groups)
        self.image = image
        self.rect = self.image.get_rect(center = (x,y-20))
        self.speed = 0# when moving 800
        self.direction = pygame.math.Vector2(0,-1)# goes up only
    def fire(self):
        self.speed = 700
    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top < 0:
            self.kill()

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
        if self.rect.top > window_height:
            self.kill()


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
image_laser = pygame.image.load('source_files/images/laser.png')
laser = Laser(all_sprites,20,window_height-20,image_laser)
# load image for stars and create stars
image_star = pygame.image.load('source_files/images/star.png')# load before so we wont have to load 20 times the same image
for i in range(20):
    star = Star(all_sprites,image_star)
#load image for meteor
image_meteor = pygame.image.load('source_files/images/meteor.png')

player = Player(all_sprites)

#timers and events -> meteor event

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 1000)


# game loop
while running:
    dt = clock.tick(FPS_target) /1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            meteor_new = Meteor(all_sprites,randint(0,window_width),0,image_meteor)

    #update
    all_sprites.update(dt)
    #draw game

    screen.fill('black')#fill with blue color
    all_sprites.draw(screen)
    pygame.display.update()# or flip - flip updates a part of the window , update the whole window



pygame.quit()
