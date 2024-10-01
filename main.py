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
# for player movment - may change
player_speed = 300
player_dir = []# ends up as a list of 4 vectors for movment in diffrent axis
player_dir.append(pygame.math.Vector2(0,1))#down index 0
player_dir.append(pygame.math.Vector2(2,0))# right 1
player_dir.append(pygame.math.Vector2(0,-1))# up 2
player_dir.append(pygame.math.Vector2(-2,0))# left 3
player_direction = pygame.math.Vector2()
#load objects

laser_surf = pygame.image.load('source_files/images/laser.png')
laser_rect = laser_surf.get_rect(center = (window_width/2,window_height-200))

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
    #new movment system
    player_direction.x = 1.5*(int(keys[pygame.K_RIGHT]) -int(keys[pygame.K_LEFT]))
    player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    player_rect.center += player_direction * player_speed * dt
    '''
        if keys[pygame.K_DOWN] and player_rect.bottom < window_height :
            player_rect.center += player_dir[0] * player_speed * dt
            player_dir2 = pygame.math.Vector2(0,1)
        if keys[pygame.K_RIGHT] and player_rect.right < window_width:# right
            player_rect.center += player_dir[1] * player_speed * dt
            player_dir2 = pygame.math.Vector2(1,0)
        if keys[pygame.K_UP]  and player_rect.top > 0:# up
            player_rect.center += player_dir[2] * player_speed * dt
            player_dir2 = pygame.math.Vector2(0,-1)
        if keys[pygame.K_LEFT] and player_rect.left > 0:# left
            player_rect.center += player_dir[3] * player_speed * dt
    '''
    #draw game
    screen.fill('azure3')#fill with blue color
    for pos in star_pos :
        screen.blit(star_surf,pos)


    screen.blit(player_surf,player_rect)
    screen.blit(laser_surf,laser_rect)
    screen.blit(meteor_surf,meteor_rect)
    pygame.display.update()# or flip - flip updates a part of the window , update the whole window

pygame.quit()
