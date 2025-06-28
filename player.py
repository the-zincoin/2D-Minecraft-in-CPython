import pygame
def renderPlayer(screen,res,config):
    surfacePlayer = pygame.surface.Surface((res,res*2))
    surfacePlayer.fill((255,255,255)) #in the future player will be a 2d model instead of a white rectangle
    playerRect = surfacePlayer.get_rect(midtop=(config.length/2,config.height/2-res)) #shift player to midtop to look centered and pleasing to look at
    screen.blit(surfacePlayer,playerRect) 