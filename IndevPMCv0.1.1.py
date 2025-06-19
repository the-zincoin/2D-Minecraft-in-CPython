import pygame,json,math,ast,random
import Perlin2d as Perl
import WorldClasses as WC
import RNGMinecraft as RNG

#load Adjustable Variables
loaded_data = {}
with open('PMDataFiles/AdjustableParameters.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        if line != lines[0]:
            if ': ' in line:
                key, value = line.split(': ', 1) 
                try:
                    parsed_value = ast.literal_eval(value)
                except (ValueError, SyntaxError):
                    parsed_value = value
                loaded_data[key] = parsed_value


#Loaded variables
height = int(1000 if loaded_data['height'] > 1000 else loaded_data['height']) #height of screen (fixed at 1000 and lower)
length = int(1400 if loaded_data['length'] > 1400 else loaded_data['length']) #length (x) of screen (fixed at 1400 and lower)
resolutionInTile = 9#int(10 if loaded_data['resolutionInTile(InPixel)'] < 10 else loaded_data['resolutionInTile(InPixel)']) #(fixed at 10 and higher)
velocity =  10#int(loaded_data['velocity'])# speed of movement
velocity = velocity if velocity < resolutionInTile*16 else resolutionInTile*16 #wraps velocity to maximum 1 chunk per tick to counter unfixed bug
currentxpos = 0
currentypos = 0
currentCachenum = 0
currentTilenum = 0
toPress = True #to prevent more than one input per tick
run=True
#Initialize spawn
xOffSet = 0
yOffSet = 0
seed = random.randint(0,2**32) if int(loaded_data['seed']) == 0 else int(loaded_data['seed']) #seed for perlinNoise @Perlin 2d
maxFrameRate = int(loaded_data['maxFrameRate'])

clock = pygame.time.Clock() #clock to track ticks per second

screen = pygame.display.set_mode((length,height-resolutionInTile*2)) #initialize window

atlas = pygame.image.load('ImageFiles/blockAtlas.png')

loadedTiles = {}

with open('PMDataFiles/BlockImagesFull.json', 'r') as file:
    blockImageNames = list(json.load(file))
lengthSide = 32

def getTile(fileName):
    global lengthSide
    indexOfTile = blockImageNames.index(fileName)
    y = math.floor(indexOfTile/lengthSide)
    x = indexOfTile % lengthSide
    print(x,y)
    rectOftile = pygame.Rect(x*16,y*16,16,16)
    tile = atlas.subsurface(rectOftile)
    return pygame.transform.scale(tile,(resolutionInTile,resolutionInTile))

def checkIfTileLoaded(fileName):
    if fileName in loadedTiles.keys():
        newtile = loadedTiles[fileName]
    else:
        newtile = getTile(fileName)
        newDict  = {fileName:newtile}
        loadedTiles.update(newDict)
    return newtile

sky = pygame.transform.scale(atlas.subsurface(pygame.Rect(0,31*16,16,16)),(resolutionInTile,resolutionInTile))
void = pygame.transform.scale(atlas.subsurface(pygame.Rect(16,31*16,16,16)),(resolutionInTile,resolutionInTile))

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
worldData = WC.renderingWorldClass(dataX[0],dataX[1],dataY[0],dataY[1],dataX[2],dataX[3],dataX[4],dataX[5],dataX[6],resolutionInTile,height,length,velocity,dataY[3],dataY[2],dataY[4],[],{},[])
blockYReference = [[int(y),worldData.bottomWrap-y*resolutionInTile] for y in range(0,256)] #acts as a standard y position of 256 for all tiles in all chunks 


#creeper icon
icon = pygame.image.load('ImageFiles/Minecraft-creeper-face.jpg')

pygame.display.set_icon(icon)

#caption for window
pygame.display.set_caption('ReleaseVersion0.1 Paper Minecraft Python')
#midway from spawn chunk 0 based on numChunks var
gnum = int((worldData.numChunks-1)/2) # number of chunks that fit per side of spawn chunk 0
#print(gnum)
#input bloxd data
#print('OffsetTilesBy',worldData.offsetTilesBy)


#generate blockdata for easy retrieval during display
def convertIntoBlocks(layerCurrent,offset):
    chunk = []
    #convert height int in iterable layer current into blittable surfaces for displaying
    pRVdirH = list(RNG.GeneratePRN(len(layerCurrent),25214903917,11,2**48,seed+offset,(2,4),1)) #pseudo-random Values for Dirt Level
    pRVdepH = list(RNG.GeneratePRN(len(layerCurrent),25214903917,11,2**48,seed+offset,(56,72),1)) #pseudo-random Values for Deepslate Level
    currentLayerData = []
    for n,height in enumerate(layerCurrent):
        currentLayerData = []
        currentLayerData = [sky for i in range(256-int(height))] #add Sky texture data
        dirtHeight,deepSlateHeight = pRVdirH[n],pRVdepH[n] #number of blocks of dirt and deepslate respectively
        stoneHeight = int(height) - 1 - dirtHeight - (deepSlateHeight)
        if height > deepSlateHeight:
            currentLayerData.append(checkIfTileLoaded("grass_block_side.png")) #add grass block data
            for i in range(int(height)-1 - stoneHeight - deepSlateHeight):
                currentLayerData.append(checkIfTileLoaded("dirt.png"))  #add dirt block data
        for i in range(stoneHeight):
            currentLayerData.append(checkIfTileLoaded("stone.png")) #add stone block data
        for i in range(deepSlateHeight):
            currentLayerData.append(checkIfTileLoaded("deepslate.png")) #add deepslate data
        #print(len(currentLayerData))
        chunk.append(list(currentLayerData))
    return list(chunk) 


#process chunkData into the list on currently rendered and loaded chunk list as well as the storage for chunks generated now and prior
def finalProcessing(iNow,layerCurrent):
    currChunk = convertIntoBlocks(layerCurrent,iNow*16) #get blockdata from the height values per block in chunk (layerCurrent)

    data = iNow,list(currChunk),[(iNow+gnum)*worldData.chunkInPix+worldData.leftWrap,0] #data to store
    worldData.currentRenderedChunks.append(list(data)) #currently rendered and loaded chunk list
    newChunkDict = {(iNow):tuple(currChunk)}
    worldData.chunkCache.update(newChunkDict) #storage for chunks generated now and prior


#add for left side
for i in range(gnum):
    dat = Perl.generatePerlinNoise(128, 3, 0-seed, 1, 16, 16, 16, 256, (gnum-i) * 16, 0)[0] #uses Perlin2d to generate height map for 2D Perlin noise
    layer = [dat[15-n] for n in range(len(dat))]  #swap to ensure chunks are smooth blending
    finalProcessing(i-gnum,layer)
    

#generates the 16th block of chunk -1 and 1st block of chunk 1
vals = Perl.generatePerlinNoise(128, 3, 0-seed, 1, 16, 16, 16, 256, 1 * 16, 0)[0][0],Perl.generatePerlinNoise(128, 3, seed, 1, 16, 16, 16, 256, 1 * 16, 0)[0][0]

#uses smoothstep formula that obtains a smooth curve of y values to blend terrain on each side of chunk 0 to prevent artifacts in height
def smoothstep(x):
    return x * x * (3 - 2 * x) if 0 <= x <= 1 else (0 if x < 0 else 1)


def smooth_fade(start, end):
    return [start + (end - start) * smoothstep(i / 15) for i in range(16)]

chunk = smooth_fade(vals[0], vals[1])
finalProcessing(0,chunk)


#add for right side
for i in range(gnum):
    layer = Perl.generatePerlinNoise(128, 3, seed, 1, 16, 16, 16, 256, (i+1) * 16, 0)[0]
    finalProcessing(i+1,layer)


#prepare chunkSurfaces to optimise rendering
for i in range(worldData.numChunks):
    surface = pygame.surface.Surface((worldData.chunkInPix,worldData.blockDisplayheight))
    worldData.chunkSurfaces.append(surface)



change = 0
#debug left and right
#pygame.draw.line(screen,(0,0,255),(rightWrap,350),(rightWrap,700),1)
#pygame.draw.line(screen,(255,255,255),(leftWrap,350),(leftWrap,700),1)


#display processed data in the currently rendered and loaded chunk lis
def display():
    global yOffSet,change
    #extract chunk surfaces to blit tiles
    for i in range(len(worldData.chunkSurfaces)):
        worldData.chunkSurfaces[i].fill((0,0,0))



    for i,chunk in enumerate(worldData.currentRenderedChunks):
        for x in range(16):
            for y in range(0,worldData.verticalNum):
                yrf = blockYReference[y][0]
                block = sky if yrf > 255 else (void if yrf < 0 else (checkIfTileLoaded("bedrock.png")  if yrf == 0 else chunk[1][x][255-yrf]))
                #overrides any tile at y=0 into bedrock
                worldData.chunkSurfaces[i].blit(block,block.get_rect(midleft=(x*resolutionInTile,blockYReference[y][1]))) #blit tiles on chunk Surface


    #debug
    #print(worldData.currentRenderedChunks[0][0],tuple(worldData.currentRenderedChunks[0][2]))
    #print(worldData.currentRenderedChunks[-1][0],tuple(worldData.currentRenderedChunks[-1][2]))
   

    #blit all chunkSurfaces with rendered tiles
    for i,chunk in enumerate(worldData.currentRenderedChunks):
        blocksurf = worldData.chunkSurfaces[i]
        blockrect = blocksurf.get_rect(midtop = (chunk[2][0],chunk[2][1])) #offset chunk to middle top
        screen.blit(blocksurf,blockrect)
    #debug chunk tiles and borders
    #     screen.set_at(tuple(chunk[2]), (0,255,0))
    #     pygame.draw.line(screen,(255,0,0),(chunk[2][0]-(worldData.chunkInPix/2),0),(chunk[2][0]-(worldData.chunkInPix/2),350),1)
    #     img = font.render(str(chunk[0]),True,(255,0,0))
    #     screen.blit(img,(chunk[2][0]-(worldData.chunkInPix/2),100))
    for i,block in enumerate(blockYReference):
        pygame.draw.line(screen,(255,0,0),(0,block[1]),(length,block[1]),1)


    #render debug line
    img = font.render(f'Debug: x= ({'{:.3f}'.format(-currentxpos)} pixels, {'{:.3f}'.format(-currentxpos/resolutionInTile)} blocks), y=({'{:.3f}'.format(currentypos)} pixels , {'{:.3f}'.format(currentypos/resolutionInTile)} blocks) Fps: {str(int(clock.get_fps()))} Seed: {seed}',True,(255,255,255))
    screen.blit(img,(0,800))
    #debug player position
    #pygame.draw.line(screen,(0,0,255),(length/2,0),(length/2,height),1)
    #pygame.draw.line(screen,(0,0,255),(0,height/2),(length,height/2),1)

    

processorX = 0
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
pressed = False
display()

#process newly generated chunks by Perlin2d
def processNewChunks(chunkOffset,seed,currentBlock) -> None:
    global currentCachenum,currentxpos
    #currentxpos += velocity if seed < 0 else -velocity
    currentCachenum += 1 if seed > 0 else -1


    if (currentCachenum + chunkOffset) in worldData.chunkCache.keys():
        loadedHeightData = worldData.chunkCache[currentCachenum+chunkOffset] #load in correct chunk at correct index using chunkCache that changes according to movement
        currentBlock[1] = list(loadedHeightData)
        #print(f"currentCachenum: {currentCachenum}, chunk number: {worldData.currentRenderedChunks[i][0]}")



    else:
        rawData = list(Perl.generatePerlinNoise(128, 3, seed, 1, 16, 16, 16, 256, (abs(currentCachenum)+gnum) * 16, 0)[0]) #if chunk has not been loaded a new one is generated
        data = [rawData[15-n] for n in range(len(rawData))] if seed < 0 else rawData #similar to the first process of storing left side to ensure chunks blend smoothly (only applicable if seed is - aka right side)
        newHeightData = convertIntoBlocks(data,currentBlock[2][0])
        newDict = {(currentCachenum +chunkOffset):tuple(newHeightData)}
        worldData.chunkCache.update(newDict)
        currentBlock[1] = list(newHeightData) #store the newly generated data in the storage of all chunks
    currentBlock[0] = currentCachenum + chunkOffset


#processChunks(-gnum,currentCachenum,-seed)
while run:


    #close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    #get current key pressed
    keyPressed = pygame.key.get_pressed()


    #render and process new and loaded chunks from cache and currentRenderedChunks


    if keyPressed[pygame.K_LEFT]:
        pressed = True
        currentxpos += velocity


        for i,value in enumerate(worldData.currentRenderedChunks):
            currChunk = value[2][0]

            if currChunk < worldData.rightWrap:
                xOffSet += velocity
                
            else:
                xOffSet = 0-(currChunk-worldData.leftWrap) - (worldData.rightWrap-currChunk) -worldData.chunkInPix + velocity #wraps the new chunk behind the opposite side (chunk clipping)
                processNewChunks(-gnum,0-seed,value)
            worldData.currentRenderedChunks[i][2][0] += xOffSet #change chunks by velocity and whether chunk needs to be wrapped
            xOffSet  = 0



    if keyPressed[pygame.K_RIGHT]:
        pressed = True
        currentxpos -= velocity


        for i,value in enumerate(worldData.currentRenderedChunks):
            currChunk = value[2][0]


            if currChunk > worldData.leftWrap:
                xOffSet -= velocity


            else:
                xOffSet = (worldData.rightWrap - currChunk) +(currChunk-worldData.leftWrap)+worldData.chunkInPix  - velocity #wraps the new chunk behind the opposite side (chunk clipping)
                processNewChunks(gnum,seed,value)
            worldData.currentRenderedChunks[i][2][0] += xOffSet #change chunks by velocity and whether chunk needs to be wrapped
            xOffSet  = 0



    if keyPressed[pygame.K_UP]:
        pressed = True
        currentypos += velocity



        for i,value in enumerate(blockYReference):
            currTile = value[1]


            if currTile < worldData.bottomWrap:
                yOffSet += velocity
                tileLOffset = 0


            else:
                yOffSet = 0-(currTile-worldData.topWrap) - (worldData.bottomWrap-currTile)  -resolutionInTile+ velocity
                tileLOffset = worldData.verticalNum #changes the index of rendering as the new tile displayed is at a different position after being wrapped around (- as you move to before previous index 0)
            blockYReference[i][1] += yOffSet
            blockYReference[i][0] += tileLOffset
            yOffSet = 0



    if keyPressed[pygame.K_DOWN]:
        currentypos -= velocity
        pressed = True


        for i,value in enumerate(blockYReference):
            currTile = value[1]


            if currTile > worldData.topWrap:
                yOffSet -= velocity
                tileLOffset = 0


            else:
                yOffSet = (worldData.bottomWrap - currTile) +(currTile-worldData.topWrap) +resolutionInTile- velocity
                tileLOffset = -worldData.verticalNum
            blockYReference[i][1] += yOffSet
            blockYReference[i][0] += tileLOffset #changes the index of rendering as the new tile displayed is at a different position after being wrapped around (+ as you move to after previous index 255)
            yOffSet = 0
    print(pygame.mouse.get_pos())
    #render chunks and player
    if pressed == True: #ensures that only chunks are re rendered when a key is actually pressed, boosting fps
        display()
        #render player
        surfacePlayer = pygame.surface.Surface((resolutionInTile,resolutionInTile*2))
        surfacePlayer.fill((255,255,255)) #in the future player will be a 2d model instead of a white rectangle
        playerRect = surfacePlayer.get_rect(midtop=(length/2,height/2-resolutionInTile)) #shift player to midtop to look centered and pleasing to look at
        screen.blit(surfacePlayer,playerRect)
        pressed = False
    clock.tick(maxFrameRate) #sets fps/tps
    pygame.display.flip() #update display

pygame.quit()