
import os
import json,pygame,math
from WCD import Chunk
#special encoder
oldWorldData = {}
class ChunkEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Chunk):
            return {
                'state': obj.state,
                'blockData': obj.blockData,
            }
        return super().default(obj)
#convertSurfaces into files for usability
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


def convertBlockData(data,cS,res,type,path):
    if type == 1:
        surface = pygame.Surface((cS,cS))
        index = 0
        for x in range(16):
            for y in range(16):
                surface.blit(data.blockData[x][y],((index//16)*res,(index%16)*res))
                index += 1
        pygame.image.save(surface,path)
    elif type == 2:
        surf=  pygame.image.load(path)
        chunk = []
        for x in range(16):
            row  = []
            for y in range(16):
                rect=  pygame.Rect(x*res,y*res,res,res)
                row.append(surf.subsurface(rect))
            chunk.append(row)
        return chunk
                


def conversionTupleAndStr(data,cS,res,type,path):
    from ast import literal_eval
    if type == 1:
        convtDat = {}
        for key,value in data.items():
            convertBlockData(value,cS,res,1,f"{path}/{key}.png")
            convtDat[str(key)] = f"{key}.png"
        return convtDat
    

    elif type == 2:
        convtDat = {}
        for key,value in data.items():
            convtDat[literal_eval(key)] = Chunk(False,convertBlockData(0,cS,res,2,f"{path}/{value}"))
        return convtDat
    

def saveWorld(worldName,seed,gameData,currPlayerPos):
    os.makedirs(f"Worlds/{worldName}",exist_ok=True)
    os.makedirs(f"Worlds/{worldName}/surfaces",exist_ok=True)
    data = {}
    cS,res = gameData.chunkSize,gameData.tileRes
    data['loadedChunks'] = conversionTupleAndStr(gameData.loadedChunks,cS,res,1,f"Worlds/{worldName}/surfaces")
    data['currentPlayerPos'] = currPlayerPos
    data['chunkCache'] = conversionTupleAndStr(gameData.chunkCache,cS,res,1,f"Worlds/{worldName}/surfaces")
    data['renderDistance'] = gameData.renderDistance
    data['seed'] = seed
    surfaces = [processSurface(gameData.chunkSurfaces,cS),processSurface(gameData.waitListSurfaces,cS)]
    pygame.image.save(surfaces[0][1],f"Worlds/{worldName}/surfaces/chunkSurfaces.png")
    pygame.image.save(surfaces[1][1],f"Worlds/{worldName}/surfaces/waitListSurfaces.png")
    data['surfaceData'] = (surfaces[0][0],surfaces[1][0],cS,list(gameData.chunkSurfaces.keys()))
    with open(f"Worlds/{worldName}/world.json", "w") as file:
        json.dump(data,file,indent=4,cls=ChunkEncoder)


def loadSurface(img,length,size):
    surface = []
    for i in range(length):
        subSurf=  pygame.Rect((i%length)*size,(i//length)*size,size,size)
        surface.append(img.subsurface(subSurf))
    return surface


def loadWorld(worldName):
    path = f"Worlds/{worldName}"
    if os.path.exists(path):
        with open(f"{path}/world.json","r") as file:
            worldData = json.load(file)
        cSImg= pygame.image.load(f"{path}/surfaces/chunkSurfaces.png") 
        wLSImg = pygame.image.load(f"{path}/surfaces/waitListSurfaces.png")
        waitListSurfaces = list(loadSurface(wLSImg,int(worldData['surfaceData'][1]),worldData['surfaceData'][2]))
        chunkSurfaces = {}
        for i,val in enumerate(loadSurface(cSImg,int(worldData['surfaceData'][0]),worldData['surfaceData'][2])):
            chunkSurfaces[tuple(worldData['surfaceData'][3][i])] = val
        worldData['loadedChunks'] = conversionTupleAndStr(worldData['loadedChunks'],worldData['surfaceData'][2],worldData['surfaceData'][2]/16,2,f"{path}/surfaces")
        worldData['chunkCache'] = conversionTupleAndStr(worldData['chunkCache'],worldData['surfaceData'][2],worldData['surfaceData'][2]/16,2,f"{path}/surfaces")
        return True,worldData,chunkSurfaces,waitListSurfaces
    else:
        print("The world does not exist.")
        return False
    