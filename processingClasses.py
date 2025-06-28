import pygame,json
from configWorld import loaded_data
with open("structures/natural/oak_tree.json","r") as file:
    oakTree = json.load(file)
oakTree = {int(key):value for key,value in oakTree.items()}



class Chunk:
    def __init__(self,state,blockData):
        self.blockData = blockData
        self.state = state
    def render(self,gameData,coord):
        try:        
            gameData.waitListSurfaces[0].fill((128,188,252)if coord[1] > gameData.checkLength else (0,0,0))
            for x in range(16):
                for y in range(16):
                    if self.blockData[x][y] == "":
                        continue
                    else:
                        gameData.waitListSurfaces[0].blit(self.blockData[x][y],(x*gameData.tileRes,y*gameData.tileRes))
        except IndexError:
            gameData.waitListSurfaces[0].fill((0,0,0))


class PerlinProperties:
    def __init__(self,A,C,M,firstSeed,permutationTable,gradients,chunkNum,chunkLength,perlinNoiseMap):
        self.A = A
        self.C = C
        self.M = M
        self.firstSeed = firstSeed
        self.permutationTable = permutationTable
        self.gradients = gradients
        self.chunkNum = chunkNum
        self.chunkLength = chunkLength
        self.perlinNoiseMap = perlinNoiseMap



class renderingWorldClass:


    def __init__(self,chunkCache,chunkSurfaces,loadedChunks):
        self.chunkCache = chunkCache
        self.chunkSurfaces = chunkSurfaces
        self.loadedChunks = loadedChunks
        self.maxLightLevel = 15


    def processChunks(self,verticalNum,rangeY,totalXChunks,totalYChunks,tileRes,chunkSize,seed,chunk0Data,fps,velocity):
        self.verticalNum = verticalNum
        self.totalXChunks = totalXChunks
        self.tileRes = tileRes
        self.chunkSize = chunkSize
        self.totalYChunks = totalYChunks
        self.rangeY = rangeY
        self.chunkLength = 16
        self.worldHeight= 320
        self.seed = seed
        self.chunksToRemove = []
        self.chunk0Data = chunk0Data
        self.waitListSurfaces = [pygame.Surface((self.chunkSize,self.chunkSize)) for i in range(self.totalXChunks*self.totalYChunks*2)]
        self.velocity = round((velocity*self.tileRes)/fps)


    def player(self,currentPlayerX,currentPlayerY):
        self.currentPlayerX = currentPlayerX
        self.currentPlayerY = currentPlayerY
    
    
    
    def graphicFiles(self):
        self.fontMojangles =  pygame.font.Font("fonts/mojanglesfontRegular.otf", 33)
        self.rectOfTile = pygame.Rect(0,0,16,16)
        self.tree = oakTree
        self.blockImageNames = list(json.load(open('textures/blockMetaData/BlockImagesFull.json', 'r')))
        self.atlas = pygame.image.load('textures/blockTextures/blockAtlas.png')
        self.sky2 = pygame.transform.scale(self.atlas.subsurface(pygame.Rect(0,31*16,16,16)),(self.tileRes,self.tileRes))

    def updateProcessor(self,newRY,totalXC,totalYC,vertNum,newChunkSize,newTR):
        self.rangeY = newRY
        self.totalXChunks = totalXC
        self.totalYChunks= totalYC
        self.verticalNum = vertNum
        self.chunkSize = newChunkSize
        self.tileRes = newTR
    def FOV(self,half,checkLength):
        self.half = half
        self.checkLength = checkLength




