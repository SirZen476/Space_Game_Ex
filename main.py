#project was made with files from Clear code
#https://github.com/clear-code-projects/5games

import pygame

#general setup
#pygame.init()# init pygame
window_width,window_height = 1280, 720#screen size
screen = pygame.display.set_mode((window_width,window_height))# create screen
pygame.display.set_caption('Space Shooter')
running = True

surf = pygame.Surface((100,200))
surf.fill('orange')
x = 100
y = 200
# import image
player_surf = pygame.image.load('/space shooter/images/player.png')

while True:
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()

    #draw game
    screen.fill('azure3')#fill with blue color
    x+= 0.1
    screen.blit(surf,(x,y))
    pygame.display.update()# or flip - flip updates a part of the window , update the whole window


pygame.quit()
