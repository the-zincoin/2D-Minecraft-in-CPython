import os
import json,pygame,math
from classes.processingClasses import Chunk
from ast import literal_eval
#special encoder
oldWorldData = {}
class ChunkEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Chunk):
            return {
                "state": obj.state,
                'blockData': obj.blockData
            }
        return super().default(obj)

#convertSurfaces into files for usability
def isSurfaceBlack(surface):
    pixel_array = pygame.surfarray.pixels3d(surface)
    return (pixel_array == [0, 0, 0]).all()

def loadFile(path):
    with open(path,"r") as file:
        return json.load(file)
def dumpFile(path,data,tag):
    with open(path,tag) as file:
        json.dump(data,file,indent=4,cls=ChunkEncoder)


def loadImageAssets(fileDict,configSlider):
    from lighting import enlighten as enl
    from classes.guiClasses import Slider
    newDict = {"orgScreenSurf":{},"orgButtons":{},"orgSliders":{}}
    for key,assetType in fileDict.items():
        for i,asset in enumerate(assetType):
            if key != "orgSliders":
                loadedImage = pygame.image.load(f"textures/widgets/{asset[0]}.png").copy()
                data = loadedImage,loadedImage.get_rect(center = tuple(asset[1]))
                dimensions = loadedImage.get_size()
                pygame.draw.rect(loadedImage,(0,0,0),(0,0,dimensions[0],dimensions[1]),3)
                newDict[key].update({asset[0]:list(data)})
            else:
                backGroundSlider = enl(pygame.transform.scale(configSlider.button,asset[1]),0.5)
                bSRect= backGroundSlider.get_rect(center = asset[2])
                sRect = configSlider.sliderScaled.get_rect(center = asset[2])
                text = asset[0]
                newDict[key].update({text:Slider(asset[1],backGroundSlider,configSlider.sliderScaled,text,(bSRect,sRect),(asset[3]),asset[2])})
    #print(newDict)
    return newDict




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

def dumpWorldData(path,gameData,currPlayerPos,seed,config):
    data = {}
    data['currentPlayerPos'] = currPlayerPos
    data['Render Distance'] = config.interactiveData["settings"]["Render Distance"]
    data['seed'] = seed
    wLSData = processSurface(gameData.waitListSurfaces,gameData.chunkSize)
    dumpFile(f"{path}/gameSaveData/surfaceMetadata.json",(wLSData[0],gameData.chunkSize,list(gameData.chunkSurfaces.keys())),"w")
    dumpFile(f"{path}/gameSaveData/gameStateData.json",data,"w")
    dumpFile(f"{path}/gameSaveData/chunkAttributes.json",determineAttr(gameData),"w")
    pygame.image.save(wLSData[1],f"{path}/gameSaveData/waitListSurfaces.png")

def dumpData(gameData, path, currPlayerPos, seed,newChunks,config):
    #print("Render Distance  @ time of Save",config.interactiveData["settings"]["Render Distance"])
    for chunkPos in newChunks:
        dumpChunkData(path,chunkPos, gameData)
    
    nPath = path.removesuffix('/chunks')
    dumpWorldData(nPath,gameData,currPlayerPos,seed,config)
def initFolders(folderList,path):
    for chunk in folderList:
        os.makedirs(f"{path}/chunk{chunk}")

def saveWorld(worldName,seed,gameData,currPlayerPos,oldData,config):
    if not os.path.exists(f"WorldSave/{worldName}"):
        os.makedirs(f"WorldSave/{worldName}")
        os.makedirs(f"WorldSave/{worldName}/chunks")
        os.makedirs(f"WorldSave/{worldName}/gameSaveData")
    cS,res = gameData.chunkSize,gameData.tileRes
    newChunks = list(set(gameData.chunkCache.keys()) - oldData)
    initFolders(newChunks,f"WorldSave/{worldName}/chunks")
    dumpData(gameData,f"WorldSave/{worldName}/chunks",currPlayerPos,seed,newChunks,config)


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
    path = f"WorldSave/{worldName}"
    if os.path.exists(path):
        surfaceMetaData = loadFile(f"{path}/gameSaveData/surfaceMetadata.json")
        surfacesForChunks = loadChunkAttributes(loadFile(f"{path}/gameSaveData/chunkAttributes.json"),f"{path}/chunks",surfaceMetaData)
        worldData = loadFile(f"{path}/gameSaveData/gameStateData.json")
        wLSImg = pygame.image.load(f"{path}/gameSaveData/waitListSurfaces.png")
        waitListSurfaces = list(loadSurface(wLSImg,int(surfaceMetaData[0]),surfaceMetaData[1]))
        chunkSurfaces = {}
        chunkSurfaces = surfacesForChunks[0]
        worldData['loadedChunks'] = surfacesForChunks[1]
        worldData['chunkCache'] = loadChunkCacheSurfaces(surfaceMetaData,f"{path}/chunks")
        return True,worldData,chunkSurfaces,waitListSurfaces
    else:
        print("The world does not exist.")
        return False 