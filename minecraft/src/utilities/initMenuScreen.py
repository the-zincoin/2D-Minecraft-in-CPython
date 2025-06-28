import random
def getCurrentElementData(config,element,init):
    offsetsButtons = config.offsetsButtons
    if element["elementType"] == "i": 
        currentElementData = init.inputBoxArgs(element,offsetsButtons,config)   
    else:
        if element["elementType"] == "chab":
            currentElementData = init.chabArgs(element,offsetsButtons)  
        else:
            if element["elementType"] == "chob":
                currentElementData = init.chobArgs(element,offsetsButtons,config)
            else:
                currentElementData = init.sliderArgs(element,config,offsetsButtons)
    return currentElementData
def init(config):
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))
    from loaderAndUnloader import loadFile
    from classes.guiClasses import Menu,classManager
    initClassManager = classManager()
    menuscreenData = loadFile("config/menuscreenData.json")
    gameMenuScreenData = {}
    for identifier,data in menuscreenData.items():
        menuscreendata = {}
        for element in data["config"]:
            if element["position"][0] == "half":
                element["position"][0] = int(config.length/2)  # Use '=' for assignment
            if element["position"][1] == "half":  # No need for elif; both conditions can be checked independently
                element["position"][1] = int(config.height/2)
            
            menuscreendata.update(getCurrentElementData(config,element,initClassManager))
        bG = pygame.image.load(f"textures/widgets/{data["backGround"]}.png") if data["backGround"] != "" else ""
        gameMenuScreenData[identifier] = Menu([menuscreendata,data["text"]],(identifier,bG,data["type"],data["previousScreen"]))
    return gameMenuScreenData

def checkStringConditions(s):
    onlyzero = '0' in s and all(char in '0 ' for char in s)
    spaces = s.strip() == ""
    return onlyzero or spaces


#handles outcome whereby world is called
def generateWorld(array,config):
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
            "Render Distance":config.interactiveData["settings"]['Render Distance'],
            "seed":seed,'surfaceData':(0,0,0,0)},{},[]]
    print("World Successfully Generated!")#,modData[0]["currentPlayerPos"])
    return seed,name,modData




def loadWorldCS(array):
    from loaderAndUnloader import loadWorld
    worldSave = loadWorld(array[0].strip())
    if worldSave[0]:
        seed = worldSave[1]['seed']
        name = array[0]
        modData = list(worldSave[1:4])
        print("World Successfully Loaded!")
        return seed,name,modData



def processInput(outcome,config):
    data = [config.interactiveData["worldAttr"][element] for element in outcome]
    if len(outcome) > 1:
        worldData = generateWorld(data,config)
    else:
        worldData= loadWorldCS(data)
    return worldData
