import pygame
from WCD import length,height
def renderPlayer(screen,res):
    surfacePlayer = pygame.surface.Surface((res,res*2))
    surfacePlayer.fill((255,255,255)) #in the future player will be a 2d model instead of a white rectangle
    playerRect = surfacePlayer.get_rect(midtop=(length/2,height/2-res)) #shift player to midtop to look centered and pleasing to look at
    screen.blit(surfacePlayer,playerRect) 