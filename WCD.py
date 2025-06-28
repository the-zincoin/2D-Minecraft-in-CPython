#attributes for rendering and perlinNoise

#contains World Common Data
import ast,pygame,json
pygame.init()
pygame.font.init()
loaded_data = {}
with open('PMDataFiles/AdjustableParameters.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if ': ' in line and line != lines[0]:
            key, value = line.split(': ', 1) 
            try:
                parsed_value = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                parsed_value = value
            loaded_data[key] = parsed_value
height = int(loaded_data['height']) #height of screen (fixed at 1000 and lower) BUG FIXED
length = int(loaded_data['length']) #length (x) of screen (fixed at 1400 and lower) BUG FIXED 
offsets = (2000-length)/2,(1000-height)/2
#velocity = velocity% (16*resolutionInTile)



class Chunk:
    def __init__(self, state, blockData):
        self.state = state
        self.blockData = blockData


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


    def __init__(self,chunkCache,chunkSurfaces,loadedChunks,velocity):
        self.chunkCache = chunkCache
        self.chunkSurfaces = chunkSurfaces
        self.loadedChunks = loadedChunks
        self.velocity=  velocity
        self.maxLightLevel = 15


    def processChunks(self,verticalNum,renderDistance,rangeY,totalXChunks,totalYChunks,tileRes,chunkSize,seed,chunk0Data):
        self.verticalNum = verticalNum
        self.totalXChunks = totalXChunks
        self.tileRes = tileRes
        self.chunkSize = chunkSize
        self.totalYChunks = totalYChunks
        self.renderDistance = renderDistance
        self.rangeY = rangeY
        self.chunkLength = 16
        self.worldHeight= 320
        self.seed = seed
        self.chunksToRemove = []
        self.chunk0Data = chunk0Data
        self.waitListSurfaces = [pygame.Surface((self.chunkSize,self.chunkSize)) for i in range(self.totalXChunks*self.totalYChunks*2)]
    


    def player(self,currentPlayerX,currentPlayerY):
        self.currentPlayerX = currentPlayerX
        self.currentPlayerY = currentPlayerY
#WRD = renderingWorldClass(gameData[0]['chunkCache'],gameData[1],gameData[2],gameData[0]['loadedChunks'],dataY[1],renderDistance,dataY[2],dataX[0],dataY[0],dataX[2],dataX[3],16,velocity,320,15,gameData[0]['currentPlayerPos'][0],gameData[0]['currentPlayerPos'][1])
#self,chunkCache,chunkSurfaces,waitListSurfaces,loadedChunks,verticalNum,renderDistance,rangeY,totalXChunks,totalYChunks,tileRes,chunkSize,chunkLength,velocity,worldHeight,maxLightLevel,currentPlayerX,currentPlayerY
    
    
    
    def graphicFiles(self,images,imageAssets):
        self.images = images
        self.imageAssets = imageAssets
        self.fontMojangles =  pygame.font.Font("fonts/mojangles.ttf", 28)
        self.rectOfTile = pygame.Rect(0,0,16,16)
        self.tree = {-2:[("oak_leaves.png",2),("oak_leaves.png",3)],
        -1:[("oak_leaves.png",2),("oak_leaves.png",3),("oak_leaves.png",4),("oak_leaves.png",5)],
        0:[("oak_log.png",0),("oak_log.png",1),("oak_log.png",2),("oak_log.png",3),("oak_leaves.png",4),("oak_leaves.png",5)],
        1:[("oak_leaves.png",2),("oak_leaves.png",3),("oak_leaves.png",4),("oak_leaves.png",5)],
        2:[("oak_leaves.png",2),("oak_leaves.png",3)]}
        self.blockImageNames = list(json.load(open('PMDataFiles/BlockImagesFull.json', 'r')))
        self.atlas = pygame.image.load('ImageFiles/blockAtlas.png')
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

    def updateFOV(self,newhalf,newcheckLength):
        self.half = newhalf
        self.checkLength = newcheckLength

def prepareX(rD,length):
    numHorizontalChunks = rD*2+1
    tileRes = int(round(length/(numHorizontalChunks*16))) + 2
    chunkSize = 16 * tileRes
    return numHorizontalChunks,16,tileRes,chunkSize


def prepareY(height,chunkSize,tileRes):
    rangeY = int(round(round(height/chunkSize) - 1) / 2) + 2
    totalYChunks = rangeY*2+1
    verticalNum = totalYChunks * tileRes 
    return totalYChunks,verticalNum,rangeY


def processRawGameData(gameData,chunk0Data,images,imageAssets):
    print("GD",gameData,type(gameData[0]))
    renderDistance = gameData[0]['renderDistance']
    velocity =  55 #int(loaded_data['velocity'])# speed of movement
    dataX = prepareX(renderDistance,length)
    dataY = prepareY(height,dataX[3],dataX[2])
    wrdInit = renderingWorldClass(gameData[0]['chunkCache'],gameData[1],gameData[0]['loadedChunks'],velocity)
    wrdInit.processChunks(dataY[1],renderDistance,dataY[2],dataX[0],dataY[0],dataX[2],dataX[3],gameData[0]['seed'],chunk0Data)
    wrdInit.player(gameData[0]['currentPlayerPos'][0],gameData[0]['currentPlayerPos'][1])
    wrdInit.graphicFiles(images,imageAssets)
    wrdInit.FOV((length//2- dataX[3]/2,height //2- dataX[3]/2),dataY[0]/2)
    return wrdInit


maxFrameRate = int(loaded_data['maxFrameRate'])
currentCachenum = 0
currentTilenum = 0
yOffSet = 0
xOffSet = 0
pygame.quit()