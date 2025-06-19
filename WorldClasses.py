#attributes for rendering and perlinNoise
#load Adjustable Variables
import ast,math

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


height = int(loaded_data['height']) #height of screen (fixed at 1000 and lower) BUG HALF-FIXED
length = int(loaded_data['length']) #length (x) of screen (fixed at 1400 and lower) BUG HALF-FIXED 
resolutionInTile = int(loaded_data['resolutionInTile(InPixel)']) #(fixed at 10 and higher) BUG FIXED
velocity =  int(loaded_data['velocity'])# speed of movement
velocity = velocity if velocity < resolutionInTile*16 else resolutionInTile*16 #wraps velocity to maximum 1 chunk per tick to counter unfixed bug FIX BUG



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
    def __init__(self,leftWrap,rightWrap,topWrap,bottomWrap,numChunks,numTiles,lengthDisplay,chunkInPix,offsetChunksBy,resolutionInTile,height,length,velocity,blockDisplayHeight,verticalNum,offsetTilesBy,currentRenderedChunks,chunkCache,chunkSurfaces):
        self.leftWrap = leftWrap
        self.rightWrap = rightWrap
        self.topWrap = topWrap
        self.bottomWrap = bottomWrap
        self.numChunks = numChunks
        self.numTiles = numTiles
        self.lengthDisplay = lengthDisplay
        self.chunkInPix = chunkInPix
        self.offsetChunksBy = offsetChunksBy
        self.resolutionInTile=resolutionInTile
        self.height=height
        self.length = length
        self.velocity = velocity
        self.blockDisplayheight = blockDisplayHeight
        self.verticalNum = verticalNum
        self.offsetTilesBy = offsetTilesBy
        self.currentRenderedChunks = currentRenderedChunks
        self.chunkCache = chunkCache
        self.chunkSurfaces = chunkSurfaces

#calculate borders x and y
def calxBorder():
    numXChunks = int(math.ceil(length / resolutionInTile)/16) + 3  #adds 3 to prevent black areas when displaying
    numXChunks = numXChunks+1 if numXChunks%2==0 else numXChunks #adding 1 to ensure that only an odd number of chunks are displayed in screen
    numXTiles = numXChunks*16
    lengthDisplay,chunkInPix= numXTiles * resolutionInTile,16*resolutionInTile
    offsetChunksBy = 0- ((lengthDisplay - length)/2)+chunkInPix/2 #offset from side of screen to fit cleanly
    return int(offsetChunksBy),int((abs(offsetChunksBy) + length)), numXChunks,numXTiles,lengthDisplay,chunkInPix,int(offsetChunksBy)
dataX = calxBorder()



def calyBorder():
    verticalNum = int(math.ceil(height/resolutionInTile))+3 #adds 3 to prevent black areas when displaying
    verticalNum = verticalNum + 1 if verticalNum%2 == 0 else verticalNum #number of tiles that can fit in block display height
    blockDisplayheight = verticalNum*resolutionInTile #total pixels occupied by tiles from top to bottom (different from height). This is to ensure that tiles cleanly fit in screen
    offsetTilesBy = 0-((blockDisplayheight-height) /2)+resolutionInTile/2#offset from y0 that helps the tiles fit cleanly
    return int(offsetTilesBy),int((abs(offsetTilesBy) + height)),verticalNum,blockDisplayheight,int(offsetTilesBy)



dataY= calyBorder()
#sets attributes in renderingWorldClass
worldData = renderingWorldClass(dataX[0],dataX[1],dataY[0],dataY[1],dataX[2],dataX[3],dataX[4],dataX[5],dataX[6],resolutionInTile,height,length,velocity,dataY[3],dataY[2],dataY[4],[],{},[])

seed = int(loaded_data['seed']) #seed for perlinNoise @Perlin 2d
maxFrameRate = int(loaded_data['maxFrameRate'])
currentxpos = 0
currentypos = 0
currentCachenum = 0
currentTilenum = 0
yOffSet = 0