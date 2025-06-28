from numpy import random
def checkStringConditions(s):
    onlyzero = '0' in s and all(char in '0 ' for char in s)
    spaces = s.strip() == ""
    return onlyzero or spaces


#handles outcome whereby world is called
def generateWorld(array,resources):
    if checkStringConditions(array[0]):
        name = f"worldId{random.randint(2,100)}"
    else:
        name = array[0].strip()
    if checkStringConditions(array[1]):
        seed = random.randint(1,2**32)
    else:
        seed = int(array[1].replace(" ",""))

    modData = [{'loadedChunks':{},
            "chunkCache":{},
            "currentPlayerPos":(0,-1000),
            "render_distance":resources.interactive_data["settings"]['render_distance'],
            "seed":seed,'surfaceData':(0,0,0,0)},{},[]]
    print("World Successfully Generated!")#,modData[0]["currentPlayerPos"])
    return seed,name,modData




def loadWorldCS(array):
    from loader_and_saver import loadWorld
    worldSave = loadWorld(array[0].strip())
    if worldSave[0]:
        seed = worldSave[1]['seed']
        name = array[0]
        modData = list(worldSave[1:4])
        print("World Successfully Loaded!")
        return seed,name,modData



def processInput(outcome,resources):
    data = [resources.interactive_data["worldAttr"][element] for element in outcome]
    if len(outcome) > 1:
        worldData = generateWorld(data,resources)
    else:
        worldData= loadWorldCS(data)
    return worldData
