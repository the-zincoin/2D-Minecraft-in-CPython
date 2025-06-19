import pygame,time
import sys
from lighting import enlighten as enl
pygame.init()
pygame.font.init()
screen  = pygame.display.set_mode((2000,1000))
titleScreen = pygame.image.load("ImageFiles/TitleScreen.png")
openGameBG = pygame.image.load("ImageFiles/OpenGameBG.png")
buttonOptions = pygame.image.load("ImageFiles/buttonOptions.png").convert_alpha()
buttonOpenGame = pygame.image.load("ImageFiles/buttonOpenGame.png").convert_alpha()
buttonCreateNewWorld = pygame.image.load("ImageFiles/buttonCreateNewWorld.png").convert_alpha()
buttonPlaySelectedWorld = pygame.image.load("ImageFiles/buttonPlaySelectedWorld.png").convert_alpha()
orgButtons = {"buttonOptions":buttonOptions,"buttonOpenGame":buttonOpenGame,"buttonCreateNewWorld":buttonCreateNewWorld,"buttonPlaySelectedWorld":buttonPlaySelectedWorld}
rects = [buttonOptions.get_rect(topleft = (750,475)),buttonOpenGame.get_rect(topleft = (750,575)),buttonCreateNewWorld.get_rect(topleft=(600,700)),buttonPlaySelectedWorld.get_rect(topleft=(900,700))]
fontMojangles = pygame.font.Font("fonts/mojangles.ttf",28)
currentScreen = "titleScreen"
orgScreens = {"titleScreen":[titleScreen,{"t1":[False,rects[0],"buttonOptions","OpenGameBg"],"t2":[False,rects[1],"buttonOpenGame","OpenGameBg"]}],
              "OpenGameBg":[openGameBG,{"t3":[0,rects[2],"buttonCreateNewWorld","titleScreen"],"t4":[0,rects[3],"buttonPlaySelectedWorld","titleScreen"]}]}
run = True
while run:
    key = pygame.key.get_pressed()
    if key[pygame.K_ESCAPE]:
        currentScreen = "titleScreen"
        for btnName,data in orgButtons.items():
            globals()[btnName] = data
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            left,middle,right = pygame.mouse.get_pressed()
            if left:
                for btnName,data in orgScreens[currentScreen][1].items():
                    if data[1].collidepoint(mousePos):
                        globals()[data[2]] = enl(globals()[data[2]],0.5)
                        orgScreens[currentScreen][1][btnName][0] = True
                        currentScreen = data[3]

    if len(orgScreens[currentScreen]) > 1:
        for btnName,data in orgScreens[currentScreen][1].items():
            orgScreens[currentScreen][0].blit(globals()[orgScreens[currentScreen][1][btnName][2]],orgScreens[currentScreen][1][btnName][1])
    screen.fill((0,0,0))
    screen.blit(orgScreens[currentScreen][0],(0,0))
    pygame.display.update()