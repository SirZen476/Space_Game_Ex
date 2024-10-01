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
x = 100
y = 200
# import images
player_surf = pygame.image.load('source_files/images/player.png')
player_rect = player_surf.get_rect(center = (window_width/2,window_height-100))# rect to control position
player_speedx = 5# 1 is left, -1 is right
player_speedy= 5

laser_surf = pygame.image.load('source_files/images/laser.png')
laser_rect = laser_surf.get_rect(center = (window_width/2,window_height-200))

meteor_surf = pygame.image.load('source_files/images/meteor.png')
meteor_rect = meteor_surf.get_rect(center = (window_width/2,window_height/2))

star_surf = pygame.image.load('source_files/images/star.png')
star_pos= [(randint(0,window_width),randint(0,window_height)) for i in range(20)]



while running:
    clock.tick(FPS_target)
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw game
    screen.fill('azure3')#fill with blue color
    for pos in star_pos :
        screen.blit(star_surf,pos)
    #random x movement
    player_rect.x += player_speedx
    if player_rect.right > window_width or player_rect.left < 0:
        player_speedx *= -1
        #random y movement
    player_rect.bottom += player_speedy
    if player_rect.top < 0 or player_rect.bottom > window_height:
        player_speedy *= -1

    screen.blit(player_surf,player_rect)
    screen.blit(laser_surf,laser_rect)
    screen.blit(meteor_surf,meteor_rect)
    pygame.display.update()# or flip - flip updates a part of the window , update the whole window

pygame.quit()
