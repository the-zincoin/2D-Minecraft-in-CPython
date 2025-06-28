import os
import pygame,math
from processing_classes import Chunk
from file_manager import loadFile,dumpFile
from ast import literal_eval
#special encoder
oldWorldData = {}

#convertSurfaces into files for usability
def isSurfaceBlack(surface):
    pixel_array = pygame.surfarray.pixels3d(surface)
    return (pixel_array == [0, 0, 0]).all()

# def handle_cache_check(cachesize,player_position,verticalLoadDistance):
#     maximum_x_cache_length = int((cachesize-1) / 2)
#     player_chunk_x,player_chunk_y = int(player_position[0]/16),int(player_position[1]/16)
#     keep_sections = []
#     for xSection in range(-maximum_x_cache_length,maximum_x_cache_length+1):
#         for ySection in range(-verticalLoadDistance,verticalLoadDistance+1):
#             current_x_section,current_y_section = player_chunk_x+xSection,player_chunk_y+ySection
#             keep_sections.append((current_x_section,current_y_section))
#     return keep_sections

# def handle_cache_deletion(package,cache_current_size):
#     if (package[0]*(package[2]*2+1)) > cache_current_size:

# def loadImageAssets(fileDict,configSlider):
#     from lighting import enlighten as enl
#     from guiClasses import Slider
#     newDict = {"orgScreenSurf":{},"orgButtons":{},"orgSliders":{}}
#     for key,assetType in fileDict.items():
#         for i,asset in enumerate(assetType):
#             if key != "orgSliders":
#                 loadedImage = pygame.image.load(f"textures/widgets/{asset[0]}.png").copy()
#                 data = loadedImage,loadedImage.get_rect(center = tuple(asset[1]))
#                 dimensions = loadedImage.get_size()
#                 pygame.draw.rect(loadedImage,(0,0,0),(0,0,dimensions[0],dimensions[1]),3)
#                 newDict[key].update({asset[0]:list(data)})
#             else:
#                 backGroundSlider = enl(pygame.transform.scale(configSlider.button,asset[1]),0.5)
#                 bSRect= backGroundSlider.get_rect(center = asset[2])
#                 sRect = configSlider.sliderScaled.get_rect(center = asset[2])
#                 text = asset[0]
#                 newDict[key].update({text:Slider(asset[1],backGroundSlider,configSlider.sliderScaled,text,(bSRect,sRect),(asset[3]),asset[2])})
#     #print(newDict)
#     return newDict




def processSurface(surfaceIterable,cS):
    length = math.sqrt(len(surfaceIterable))
    surface = pygame.Surface((int(length)*cS,(int(length)+1)*cS))
    if isinstance(surfaceIterable,dict):
        index = 0
        for value in surfaceIterable.values():
            surface.blit(value,((index%length)*cS,(index // length)*cS))
            index += 1
    elif isinstance(surfaceIterable,list):
        for i,value in enumerate(surfaceIterable):
            surface.blit(value,((i%length)*cS,(i // length)*cS))
    return length,surface
#convert individual block data in chunk





#compile into imageFile
def convertBlockData(gameData,cS,res,type,path,surf):
    if type == 1:
        surface = pygame.Surface((cS,cS))
        void = pygame.Surface((res,res))
        void.fill((0,0,0))
        index = 0
        data = gameData.blockData
        #print("BlockData",len(data[0]),len(data))
        for x in range(16):
            for y in range(16):
                #print("Index",x,y)
                if data[x][y] == "":
                    surface.blit(void,((index//16)*res,(index%16)*res))
                else:
                    surface.blit(data[x][y],((index//16)*res,(index%16)*res))
                index += 1
        pygame.image.save(surface,path)
    elif type == 2:
        chunk = []
        for x in range(16):
            row  = []
            for y in range(16):
                rect=  pygame.Rect(x*res,y*res,res,res)
                if isSurfaceBlack(surf.subsurface(rect)):
                    row.append("")
                else:
                    row.append(surf.subsurface(rect))
            chunk.append(row)
        return chunk
    

def dumpChunkData(path,chunkPos,gameData):
    
    if not os.path.exists(f"{path}/chunk{chunkPos}/ChunkSurf.png"):
        convertBlockData(gameData.chunkCache[chunkPos],gameData.chunkSize,gameData.tileRes,1,f"{path}/chunk{chunkPos}/ChunkSurf.png","")


def determineAttr(data):
    itemDat = {}
    for key in data.chunkCache.keys():
        itemDat[str(key)] = (True if key in data.loadedChunks.keys() else False,True if key in data.chunkSurfaces.keys() else False)
    #first is wether in loadedChunks,second whether in chunkSUrfaces
    return itemDat

def dumpWorldData(path,gameData,currPlayerPos,seed,config,cache_size):
    data = {}
    data['currentPlayerPos'] = currPlayerPos
    data['render_distance'] = config.interactive_data["settings"]["render_distance"]
    data['seed'] = seed
    data['cache_size'] = cache_size 
    wLSData = processSurface(gameData.waitListSurfaces,gameData.chunkSize)
    dumpFile(f"{path}/gameSaveData/surfaceMetadata.sav",(wLSData[0],gameData.chunkSize,list(gameData.chunkSurfaces.keys())),"wb")
    dumpFile(f"{path}/gameSaveData/gameStateData.sav",data,"wb")
    dumpFile(f"{path}/gameSaveData/chunkAttributes.sav",determineAttr(gameData),"wb")
    pygame.image.save(wLSData[1],f"{path}/gameSaveData/waitListSurfaces.png")

def dumpData(gameData, path, currPlayerPos, seed,newChunks,config,cache_size):
    #print("Render Distance  @ time of Save",config.interactiveData["settings"]["Render Distance"])
    for chunkPos in newChunks:
        dumpChunkData(path,chunkPos, gameData)
    
    nPath = path.removesuffix('/chunks')
    dumpWorldData(nPath,gameData,currPlayerPos,seed,config,cache_size)
def initFolders(folderList,path):
    for chunk in folderList:
        if not os.path.exists(f"{path}/chunk{chunk}"):
            os.makedirs(f"{path}/chunk{chunk}")

def saveWorld(worldName,seed,gameData,currPlayerPos,oldData,config,cache_size,cache_max_size):
    if not os.path.exists(f"worlds/{worldName}"):
        os.makedirs(f"worlds/{worldName}")
        os.makedirs(f"worlds/{worldName}/chunks")
        os.makedirs(f"worlds/{worldName}/gameSaveData")
    cS,res = gameData.chunkSize,gameData.tileRes
    newChunks = list(set(gameData.chunkCache.keys()) - oldData)
    cache_full_size = len(newChunks) + cache_size
    initFolders(newChunks,f"worlds/{worldName}/chunks")
    dumpData(gameData,f"worlds/{worldName}/chunks",currPlayerPos,seed,newChunks,config,cache_full_size)
    #package_to_delete = cache_max_size,currPlayerPos,gameData.rangeY
    #return package_to_delete


def loadSurface(img,length,size):
    surface = []
    for i in range(length):
        subSurf=  pygame.Rect((i%length)*size,(i//length)*size,size,size)
        surface.append(img.subsurface(subSurf))
    return surface



def loadChunkAttributes(chunkDataDict,path,surfaceData):
    chunkSurfaces = {}
    loadedChunks = {}
    for chunkPos,chunkData in chunkDataDict.items():
        cP = literal_eval(chunkPos)
        surf = pygame.image.load(f"{path}/chunk{cP}/ChunkSurf.png").convert_alpha()
        if chunkData[0] == True:
            loadedChunks[cP] = Chunk(True,convertBlockData([],surfaceData[1],int(surfaceData[1]/16),2,"",surf))
        if chunkData[1] == True:
            chunkSurfaces[cP] = surf
    return chunkSurfaces,loadedChunks

def loadChunkCacheSurfaces(surfMetaDat,path):
    from pathlib import Path
    currentPath = Path(path)
    chunkCache = {}
    for folder in currentPath.iterdir():
        surf = pygame.image.load(f"{path}/{folder.name}/ChunkSurf.png")
        chunkPos = folder.name.removeprefix("chunk")
        chunkCache[literal_eval(chunkPos)] = Chunk(False,convertBlockData([],surfMetaDat[1],surfMetaDat[1]/16,2,"",surf))
    return chunkCache   


def loadWorld(worldName):
    path = f"worlds/{worldName}"
    if os.path.exists(path):
        surfaceMetaData = loadFile(f"{path}/gameSaveData/surfaceMetadata.sav","rb")
        surfacesForChunks = loadChunkAttributes(loadFile(f"{path}/gameSaveData/chunkAttributes.sav","rb"),f"{path}/chunks",surfaceMetaData)
        worldData = loadFile(f"{path}/gameSaveData/gameStateData.sav","rb")
        wLSImg = pygame.image.load(f"{path}/gameSaveData/waitListSurfaces.png")
        waitListSurfaces = list(loadSurface(wLSImg,int(surfaceMetaData[0]),surfaceMetaData[1]))
        chunkSurfaces = {}
        chunkSurfaces = surfacesForChunks[0]
        worldData['loadedChunks'] = surfacesForChunks[1]
        worldData['chunkCache'] = loadChunkCacheSurfaces(surfaceMetaData,f"{path}/chunks")
        return True,worldData,chunkSurfaces,waitListSurfaces
    print("Error: World does not exist")
    return False


