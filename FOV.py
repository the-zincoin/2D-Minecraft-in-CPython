import pygame
from WCD import length,prepareX,prepareY,height
def FOV(key,tick,gameData):
    diff = -1 if key[pygame.K_0] else (1 if key[pygame.K_1] else 0)
    if gameData.renderDistance > 1 and diff != 0 and tick == 0:
        gameData.renderDistance += diff
        newFOVX = prepareX(gameData.renderDistance, length, 16)
        newFOVY = prepareY(height,newFOVX[3],newFOVX[2])
        gameData.loadedChunks,gameData.chunkSurfaces = {},{}
        gameData.waitListSurfaces = [pygame.Surface((newFOVX[3],newFOVX[3])) for i in range(newFOVX[0]*newFOVY[0]*2)]
        gameData.updateProcessor(newFOVY[2],newFOVX[0],newFOVY[0],newFOVY[1],newFOVX[3],newFOVX[2])
        return True
    