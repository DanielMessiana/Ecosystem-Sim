import pygame
from scripts import *
from variables import *

# pygame vars
pygame.init()

X = 800
Y = 600
centerx = X / 2
centery = Y / 2

LIGHT_BROWN=(196, 164, 132)
WHITE=(255,255,255)
BLACK=(0,0,0)

DISPLAY=pygame.display.set_mode((X,Y),0,32)
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.Font('freesansbold.ttf', 52)
smallfont = pygame.font.SysFont('Corbel',35)

populationtext1 = font.render(str(rpopulation), True, BLACK)
pt1Rect = populationtext1.get_rect()
pt1Rect.center = (centerx,centery-200)

def menu():
    global populationtext1
    DISPLAY.fill(LIGHT_BROWN)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
     
                pygame.quit()
     
                quit()
            pygame.display.update()

        mouse = pygame.mouse.get_pos()

        DISPLAY.blit(populationtext1, pt1Rect)

        main()
        populationtext1 = font.render(str(rpopulation), True, BLACK)

        pygame.display.update()