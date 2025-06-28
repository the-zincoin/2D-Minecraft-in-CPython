import pygame
pygame.init()

screen  = pygame.display.set_mode((2000,1000), pygame.SCALED)
bg = pygame.image.load("assets/textures/gui/menus/originaltextures/basetextures/bgTitleScreen.png").convert_alpha()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,255))
    screen.blit(bg,(0,0))
    pygame.display.update()