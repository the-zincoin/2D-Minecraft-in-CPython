import pygame,math
from gameState import GameState
from Perlin2d import generatePerlinNoise as gPN
from configWorld2 import GameConfig
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((960,960))


#required for terrain to occur
#separate from Terrain Manager
run = True
clock = pygame.time.Clock()
    
gameConfig = GameConfig()
gameState = GameState()
print(hasattr(GameState,"playerStateVariables"))
def loadChunk(xChunk):
    """Loads chunk and check whether in cache"""
    if xChunk not in gameState.terrainStateVariables["chunkCache"]:
        # if not, generate the chunk
        gameState.terrainStateVariables["chunkCache"][xChunk] = gameConfig.getChunkTileData(gPN(gameConfig,xChunk),gameConfig.chunkSize)
    # add to loaded chunks set
    gameState.terrainStateVariables["loadedChunks"].add(xChunk)

def updateChunks(playerBlockX):
    """Updates all chunks: Removes all chunks outside render Distance and loads new chunks"""
    gameState.playerStateVariables["playerChunkX"] = math.floor(playerBlockX / 16)

    # hold all chunks to be loaded
    chunksToLoad = set() #get rid of  already loaded chunks optimisation #ONLY STORES CHUNKS NEEDED TO BE FRESHLY LOADED
    # determine the chunks within the render distance
    for xChunk in range(-gameConfig.renderDistance, gameConfig.renderDistance + 1):
        chunksToLoad.add(xChunk)

    # load all chunks in range
    for xChunk in chunksToLoad:
        loadChunk(xChunk)


    gameState.terrainStateVariables["loadedChunks"] = gameState.terrainStateVariables["loadedChunks"].intersection(chunksToLoad) #only acquire common coords

def renderChunks():
    for chunk in gameState.terrainStateVariables["loadedChunks"]:
        chunkData = gameState.terrainStateVariables["chunkCache"][chunk]
        surface = chunkData.render(gameConfig,gameState.playerStateVariables["playerBlockY"],chunkData)
        chunkXPos = ((gameState.playerStateVariables["playerChunkX"] - chunk) + 0.5) * gameConfig.chunkSize
        screen.blit(surface,(chunkXPos,0))
def mainGameLoop():
    global run
    while run:
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        key = pygame.key.get_pressed()
        gameState.playerMovement(key)
        updateChunks(gameState.playerStateVariables["playerBlockX"])
        renderChunks()
        pygame.display.update()
        clock.tick(60)
mainGameLoop()