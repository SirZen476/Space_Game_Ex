#project was made with files from Clear code
#https://github.com/clear-code-projects/5games

import pygame
from Tools.scripts.dutree import display
from sympy.core.random import randint

#general setup
#pygame.init()# init pygame, causes freeze at start - neet to see if something goes wrong
window_width,window_height = 1280, 720 #screen size
screen = pygame.display.set_mode((window_width,window_height))# create screen
pygame.display.set_caption('Space Shooter')
running = True
clock =pygame.time.Clock()  # control framerate, control
FPS_target = 99
surf = pygame.Surface((100,200))
surf.fill('orange')
# import images
player_surf = pygame.image.load('source_files/images/player.png')
player_rect = player_surf.get_rect(center = (window_width/2,window_height-100))# rect to control position
# speed of player
player_speed = 500
#for player direction
player_direction = pygame.math.Vector2()
#load objects

laser_surf = pygame.image.load('source_files/images/laser.png')
laser_rect = laser_surf.get_rect(center = (20,window_height-40))

meteor_surf = pygame.image.load('source_files/images/meteor.png')
meteor_rect = meteor_surf.get_rect(center = (window_width/2,window_height/2))

star_surf = pygame.image.load('source_files/images/star.png')
star_pos= [(randint(0,window_width),randint(0,window_height)) for i in range(20)]


while running:
    dt = clock.tick(FPS_target) /1000
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    #new movement system
    player_direction.x = (int(keys[pygame.K_RIGHT]) -int(keys[pygame.K_LEFT]))# x speed is faster
    player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])# y speed
    if (player_rect.bottom > window_height and player_direction.y > 0) or (player_rect.top < 0 and player_direction.y < 0) :
        player_direction.y = 0
    if (player_rect.right > window_width and player_direction.x>0 ) or (player_rect.left < 0 and player_direction.x<0):
        player_direction.x = 0
    if player_direction:
        player_direction = player_direction.normalize()# normalize to keep speed in diagonal movment same
    player_rect.center += player_direction* player_speed * dt

    #draw game
    screen.fill('azure3')#fill with blue color
    for pos in star_pos :
        screen.blit(star_surf,pos)


    screen.blit(player_surf,player_rect)
    screen.blit(laser_surf,laser_rect)
    screen.blit(meteor_surf,meteor_rect)
    pygame.display.update()# or flip - flip updates a part of the window , update the whole window

pygame.quit()
