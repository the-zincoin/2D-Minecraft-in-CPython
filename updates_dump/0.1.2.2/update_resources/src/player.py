import pygame
def renderPlayer(screen,res,resources):
    surfacePlayer = pygame.surface.Surface((res,res*2))
    surfacePlayer.fill((255,255,255)) #in the future player will be a 2d model instead of a white rectangle
    playerRect = surfacePlayer.get_rect(midtop=(resources.length/2,resources.height/2-res)) #shift player to midtop to look centered and pleasing to look at
    screen.blit(surfacePlayer,playerRect) 