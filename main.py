#project was made with files from Clear code
#https://github.com/clear-code-projects/5games
import random

import pygame
from Tools.scripts.dutree import display
from fontTools.merge.util import current_time
from sympy.core.random import randint
from random import randint, uniform
from pygame.sprite import Sprite

class Player(Sprite):
    def __init__(self, groups):
        super().__init__(groups)# for inheretance to init parent class
        self.image = pygame.image.load('source_files/images/player.png')
        self.rect = self.image.get_rect(center = (window_width/2,window_height-100))
        self.speed = 500
        self.direction = pygame.math.Vector2()
        # for shooting and score
        self.last_shot = 0.0
        self.cooldown = 250
        self.score = 0

        self.hp = 3
        self.hp_cooldown = 200
        self.last_hit = 0.0
        # create white image for hit animation
        self.hit_image = pygame.mask.from_surface(self.image)
        self.hit_image = self.hit_image.to_surface()
        self.hit_image.set_colorkey((0,0,0))

        self.og_image = self.image # save og image for later

    def check_hit(self):# true if hit in last interval false if not
        curr_time = pygame.time.get_ticks()
        interval = curr_time - self.last_hit
        if (interval > self.hp_cooldown) :return False
        return True

    def hit(self):
        if not self.check_hit():# meaning we are currently not after getting hit, meaning we can get hit
            self.last_hit = pygame.time.get_ticks()
            self.hp -= 1
            sound_damage.play()
            if self.hp <= 0:
                return False#meaning running is false
        return True

    def addscore(self,score):
        self.score +=score

    def update(self,dt):
        #check if still hit
        if self.check_hit():
            self.image = self.hit_image
        else:
            self.image = self.og_image

        current_time = pygame.time.get_ticks()
        interval = current_time - self.last_shot
        keys = pygame.key.get_pressed()
        #chek for shot and fire
        if(keys[pygame.K_SPACE] and interval> self.cooldown):# chack if pressed space and interval is right
            laser_fire = Laser((all_sprites,lasers_sprites), self.rect.centerx, self.rect.centery, image_laser)  # add new laser
            laser_fire.fire()#fire the laser - start movment
            self.last_shot = pygame.time.get_ticks()
            sound_laser.play()
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
        if self.rect.bottom < 0:
            self.kill()# kill sprite( remove from game

class Meteor(Sprite):
    def __init__(self,groups,x,y,image ):
        super().__init__(groups)
        self.image = image
        self.OG_image = image# original image for rotation later on
        self.rect = self.image.get_rect(center = (x,y))
        self.speed = 500
        self.direction = pygame.Vector2(uniform(-0.5,0.5),1)
        self.rotation = 0
        self.rotation_rate = randint(40,200  )

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if self.rect.top > window_height:
            self.kill()# kill if out of screen
            player.addscore(10)
        # rotate meteor -
        self.rotation  += self.rotation_rate*dt # *dt for same rotation on diffrent FPS
        self.image = pygame.transform.rotozoom(self.OG_image, self.rotation,1)# set image as rotated one
        self.rect = self.image.get_rect(center = self.rect.center)

class Explosion(Sprite):
    def __init__(self,groups,x,y,images):
        super().__init__(groups)
        self.id = 0
        self.images = images
        self.image = self.images[self.id]
        self.rect = self.image.get_rect(center = (x,y))

    def update(self, dt):
        self.id += 30 * dt
        if self.id >= len(self.images):# check if id is out of range - animation is done if true, kill sprite to not show again
            self.kill()
        else : self.image = self.images[int(self.id) ]

def Collisions():# returns true if no coll with meteor, false if coll with meteor detected, checks for coll for lasers with meteor, destroys both on hit
    for laser in lasers_sprites:
        if (pygame.sprite.spritecollide(laser, meteors_sprites, True, pygame.sprite.collide_mask)):# check if collision is happening with laser - empty list if no coll, deletes meteor that collided
            laser.kill()# delete laser
            player.addscore(100)
            Explosion(all_sprites, laser.rect.centerx, laser.rect.top, images_exp)
            sound_exp.play()
    meteors_hit = pygame.sprite.spritecollide(player, meteors_sprites, False,pygame.sprite.collide_mask)
    if meteors_hit:# pygame.sprite.collide_mask - better collision , but affects game speed - not really a factor for now
        for meteor in meteors_hit:
            meteor.kill()
        return player.hit()
    return True

def display_score():
    score_surt = font.render('Score: '+ str(player.score), True, 'white')
    score_rect = score_surt.get_rect(topleft = (20,15))
    screen.blit(score_surt, score_rect)
    pygame.draw.rect(screen, 'white', score_rect.inflate(20,15), 5,10)

def display_hp():
    hp_surt = font.render('health: '+ str(player.hp), True, 'white')
    hp_rect = hp_surt.get_rect(topleft = (20,55))
    screen.blit(hp_surt, hp_rect)
    pygame.draw.rect(screen, 'white', hp_rect.inflate(20,15), 5,10)

#general setup
pygame.init()# init pygame, causes freeze at start - neet to see if something goes wrong

window_width,window_height = 1280, 720 #screen size
screen = pygame.display.set_mode((window_width,window_height))# create screen
pygame.display.set_caption('Space Shooter')
running = True
clock =pygame.time.Clock()  # control framerate, control
FPS_target = 99

# sprites groups
all_sprites = pygame.sprite.Group()
lasers_sprites = pygame.sprite.Group()
meteors_sprites = pygame.sprite.Group()
font = pygame.font.Font('source_files/images/Oxanium-Bold.ttf', 30)
# load images
image_laser = pygame.image.load('source_files/images/laser.png')
image_star = pygame.image.load('source_files/images/star.png')# load before so we wont have to load 20 times the same image
image_meteor = pygame.image.load('source_files/images/meteor.png')
# load explosion frames :
images_exp = []
for i in range(0,21):
    images_exp.append(pygame.image.load('source_files/images/explosion/'+str(i)+'.png'))

# create laser and stars sprite for display

laser_view = Laser(all_sprites,20,window_height-20,image_laser)# for view on the side
for i in range(20):
    Star(all_sprites,image_star)
#create player

player = Player(all_sprites)# for ease of access

#timers and events -> meteor event

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 200)
# sounds!
sound_damage = pygame.mixer.Sound('source_files/audio/damage.ogg')
sound_laser = pygame.mixer.Sound('source_files/audio/laser.wav')
sound_laser.set_volume(0.5)
sound_exp = pygame.mixer.Sound('source_files/audio/explosion.wav')
sound_exp.set_volume(0.5)
sound_game = pygame.mixer.Sound('source_files/audio/game_music.wav')
sound_game.set_volume(0.4)
sound_game.play(loops = -1)

# game loop
while running:
    dt = clock.tick(FPS_target) /1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == meteor_event:
            Meteor((all_sprites,meteors_sprites),randint(0,window_width),0,image_meteor)# add to both groups

    #update
    all_sprites.update(dt)
    # collision detect:
    running = Collisions()# check for coll
    #draw game
    screen.fill('black')#fill with blue color
    all_sprites.draw(screen)
    display_score()
    display_hp()
    pygame.display.update()# or flip - flip updates a part of the window , update the whole window


pygame.quit()
