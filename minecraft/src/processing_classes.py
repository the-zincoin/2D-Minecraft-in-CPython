import pygame,json
with open("assets/config/hardcoded/game/structures/natural/oak_tree.json","r") as file:
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

#handles Variables acquired from genconsts.json to run Perlin2d
class PerlinProperties:
    def __init__(self,genconsts,seed):
        self.genconsts = genconsts
        self.seed = seed
        self.permutationTable = []
        self.perlinNoiseMap = []



class renderingWorldClass:


    def __init__(self,chunkCache,chunkSurfaces,loadedChunks):
        self.chunkCache = chunkCache
        self.chunkSurfaces = chunkSurfaces
        self.loadedChunks = loadedChunks
        self.maxLightLevel = 15


    def processChunks(self,verticalNum,rangeY,totalXChunks,totalYChunks,tileRes,chunkSize,seed,chunk0Data,velocity):
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
        self.velocity = round((velocity*self.tileRes))

    def player(self,currentPlayerX,currentPlayerY):
        self.currentPlayerX = currentPlayerX
        self.currentPlayerY = currentPlayerY
    
    
    
    def graphicFiles(self):
        self.fontMojangles =  pygame.font.Font("assets/fonts/font_mojangles_regular.otf", 33)
        self.rectOfTile = pygame.Rect(0,0,16,16)
        self.tree = oakTree
        self.tileMetaData = dict(json.load(open('assets/textures/game/block_metadata/png_block_identifier.json', 'r')))
        self.atlas = pygame.image.load('assets/textures/game/block_textures/block_atlas.png')

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




