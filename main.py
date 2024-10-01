#project was made with files from Clear code
#https://github.com/clear-code-projects/5games

import pygame
from Tools.scripts.dutree import display
from sympy.core.random import randint

#general setup
#pygame.init()# init pygame
window_width,window_height = 1280, 720#screen size
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
player_speed = 250
player_dir = []
player_dir.append(pygame.math.Vector2(0,1))#down index 0
player_dir.append(pygame.math.Vector2(1,0))# right 1
player_dir.append(pygame.math.Vector2(0,-1))# up 2
player_dir.append(pygame.math.Vector2(-1,0))# left 3


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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and player_rect.bottom < window_height:
                player_rect.center += player_dir[0] * player_speed * dt
            if event.key == pygame.K_RIGHT and player_rect.right < window_width:
                player_rect.center += player_dir[1] * player_speed * dt
            if event.key == pygame.K_UP and player_rect.top > 0:
                player_rect.center += player_dir[2] * player_speed * dt
            if event.key == pygame.K_LEFT and player_rect.left > 0:
                player_rect.center += player_dir[3] * player_speed * dt



    #draw game
    screen.fill('azure3')#fill with blue color
    for pos in star_pos :
        screen.blit(star_surf,pos)
    #random x and y movement
    '''
    player_rect.center += player_dir * player_speed * dt# player movment with vector
    if player_rect.right > window_width or player_rect.left < 0:
        player_dir[0] *= -1
    if player_rect.top < 0 or player_rect.bottom > window_height:
        player_dir[1] *= -1
    '''
    screen.blit(player_surf,player_rect)
    screen.blit(laser_surf,laser_rect)
    screen.blit(meteor_surf,meteor_rect)
    pygame.display.update()# or flip - flip updates a part of the window , update the whole window

pygame.quit()
