
from Perlin2d import generatePerlinNoise as gPN
from tiles2 import convertIntoBlocks as cB
from WCD import Chunk
def checkChunkInCache(coord, gameData,chunkData=[]):
    if coord in gameData.chunkCache:
        blockData = gameData.chunkCache[coord].blockData
    else:
        index = gameData.totalYChunks - (coord[1] + gameData.rangeY)
        blockData = [chunkData[320 * i + index * 16:320 * i + 16 + index * 16] for i in range(16)]
    gameData.loadedChunks[coord] = Chunk(True, blockData)
    gameData.chunkCache[coord] = Chunk(False, list(blockData))   

def prepareXTiles(chunkX, side,gameData):
    dat = list(gPN(256, 3, gameData.seed * side, 1,abs(chunkX) * 16))[0]
    return cB([dat[15-n] for n in range(len(dat))] if side == 1 else dat , abs(chunkX),gameData)
def updateChunks(gameData,playerX,playerY):
    playerChunkX = round(playerX / gameData.chunkSize)
    playerChunkY = round(playerY / gameData.chunkSize)

    for chunkX in range(-gameData.renderDistance, gameData.renderDistance + 1):
        currentchunkX = playerChunkX + chunkX
        chunkXdata = prepareXTiles(currentchunkX, -1 if currentchunkX < 0 else 1,gameData)
        
        for chunkY in range(-gameData.rangeY, gameData.rangeY + 1):
            currentchunkY = playerChunkY + chunkY
            if (currentchunkX, currentchunkY) not in gameData.loadedChunks:
                checkChunkInCache((currentchunkX, currentchunkY), gameData,gameData.chunk0Data if currentchunkX == 0 else chunkXdata)

    gameData.chunksToRemove = [
        chunk for chunk in gameData.loadedChunks.keys() 
        if (abs(chunk[0] - playerChunkX) > gameData.renderDistance or abs(chunk[1] - playerChunkY) > gameData.rangeY)
    ]

    for chunk in gameData.chunksToRemove:
        gameData.chunkCache[chunk].state = False if chunk in gameData.chunkCache else gameData.chunkCache.setdefault(chunk, Chunk(False, gameData.loadedChunks[chunk].blockData))
        del gameData.loadedChunks[chunk]


def playerMovement(key,gameData,pressed,currentPlayerX,currentPlayerY):
    import pygame
    if key[pygame.K_RIGHT]:
        currentPlayerX -= gameData.velocity
        pressed = True
    elif key[pygame.K_LEFT]:
        currentPlayerX += gameData.velocity
        pressed = True
    elif key[pygame.K_UP]:
        currentPlayerY += gameData.velocity
        pressed = True
    elif key[pygame.K_DOWN]:
        currentPlayerY -= gameData.velocity
        pressed = True

    if pressed:
        updateChunks(gameData,currentPlayerX, currentPlayerY)
    return currentPlayerX,currentPlayerY,pressed




