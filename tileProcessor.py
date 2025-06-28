
from RNGMinecraft import GeneratePRN as gPRN
from scalingFunction import doNormalization as dN
import lighting,math,pygame
loadedTiles = {}
def getTile(fileName,gameData):
    indexOfTile = gameData.blockImageNames.index(fileName)
    gameData.rectOfTile.x = (indexOfTile % 32)*16
    gameData.rectOfTile.y = (math.floor(indexOfTile/32))*16 
    tile = gameData.atlas.subsurface(gameData.rectOfTile)
    return pygame.transform.scale(tile,(gameData.tileRes,gameData.tileRes))
def checkIfTileLoaded(fileName,lightLevel,gameData):
    if fileName in loadedTiles.keys():
        LightLevels =loadedTiles[fileName]
    else:
        LightLevels = lighting.getAllLight(getTile(fileName,gameData))
    loadedTiles[fileName] = LightLevels
    return LightLevels[lightLevel]
def convertIntoBlocks(layerCurrent, offset,gameData):
    chunk = []
    pRVdirH = list(gPRN(len(layerCurrent), 25214903917, 11, 2**48, gameData.seed + offset, (2, 4), 1))
    pRVdepH = [int(val) for val in dN(pRVdirH, (1, 16), 1)]
    randTree = int(pRVdirH[0]*3) + 4  # Tree position index in the layer
    startHeight = int(layerCurrent[randTree]+1)
    surf = pygame.Rect(0,0,gameData.tileRes,gameData.tileRes)
    # Main block generation
    for n, height in enumerate(layerCurrent):
        h = int(height)
        dirtHeight, deepSlateHeight = pRVdirH[n], pRVdepH[n]
        skyHeight = int(gameData.worldHeight - h)
        chunk.extend([gameData.sky2] * skyHeight)
        for y in range(h):
            yRH, color = y + skyHeight, 15 - min(15,y)
            if color != 0 or y >= (h + 1):
                if y == 0 and yRH < 191:
                    chunk.append(checkIfTileLoaded("grass_block_side.png", color,gameData))
                elif y <= dirtHeight and yRH < 191:
                    chunk.append(checkIfTileLoaded("dirt.png", color,gameData))
                elif yRH < (247 + deepSlateHeight):
                    chunk.append(checkIfTileLoaded("stone.png", color,gameData))
                elif y < (h - 1):
                    chunk.append(checkIfTileLoaded("deepslate.png", color,gameData))
                else:
                    chunk.append(checkIfTileLoaded("bedrock.png", color,gameData))
            else:
                chunk.append("")
    if startHeight >= 127:
        # Adding tree at `randTree` position
        for layer, blocks in gameData.tree.items():
            for fileName, pos in blocks:
                tree_index = 320*(layer+randTree+1) - startHeight - pos
                if 0 <= tree_index < len(chunk):
                    chunk[tree_index] = checkIfTileLoaded(fileName,15,gameData)
    return chunk