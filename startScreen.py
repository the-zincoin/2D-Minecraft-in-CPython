import pygame
from WCD import loaded_data


def generateWorld(array):
    name = array[0].strip()
    seed = int(array[1].replace(" ",""))
    modData = [{'loadedChunks':{},
            "chunkCache":{},
            "currentPlayerPos":(0,0),
            "renderDistance":loaded_data['renderDistance'],
            "seed":seed,'surfaceData':(0,0,0,0)},{},[]]
    return seed,name,modData


def loadWorldCS(array):
    from loadAndUnload import loadWorld
    worldSave = loadWorld(array[0].strip())
    if worldSave[0]:
        seed = worldSave[1]['seed']
        name = array[0]
        modData = list(worldSave[1:4])
        return seed,name,modData
    

def processInput(userInput):
    array = list(userInput.split(","))
    print("AR",array)
    if len(array) > 1:
        data = generateWorld(array)
    elif len(array) == 1:
        data = loadWorldCS(array)
    return list(data)
def run(screen,currentScreen,needInput,images,imageAssets,events):
    orgScreens,orgButtons,orgScreenSurf,fontMojangles,inputs = images[0],images[1],images[2],images[3],images[4]
    from lighting import enlighten as enl
    from WCD import offsets
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            left, middle, right = pygame.mouse.get_pressed()
            mousePos = pygame.mouse.get_pos()
            if left and currentScreen != "game":
                for objName, data in orgScreens[currentScreen][1].items():
                    if "b" in objName:
                        if data[1].collidepoint(mousePos[0]+offsets[0],mousePos[1]+offsets[1]):
                            imageAssets[data[2]] = enl(imageAssets[data[2]], 0.5)
                            orgScreens[currentScreen][1][objName][0] = True
                            currentScreen = data[3]
                            needInput = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and currentScreen != "titleScreen" and needInput:
                currentScreen = orgScreens[currentScreen][2]
                for btnName, data in orgButtons.items():
                    imageAssets[btnName] = data
    if len(orgScreens[currentScreen]) > 1:
        imageAssets[orgScreens[currentScreen][0]] = orgScreenSurf[orgScreens[currentScreen][0]][0].copy()
        for objName, data in orgScreens[currentScreen][1].items():
            if "b" in objName:
                imageAssets[orgScreens[currentScreen][0]].blit(imageAssets[orgScreens[currentScreen][1][objName][2]], orgScreens[currentScreen][1][objName][1])
            elif "t" in objName:
                txt = fontMojangles.render(data[0], True, (255, 255, 255))
                imageAssets[orgScreens[currentScreen][0]].blit(txt, tuple(data[1]))

        screen.fill((0, 0, 0))
        screen.blit(imageAssets[orgScreens[currentScreen][0]],orgScreenSurf[orgScreens[currentScreen][0]][1])
        pygame.display.update()
    if needInput and currentScreen in inputs.keys():
        userInput = input(inputs[currentScreen])
        needInput = False
        currentScreen = "game"  # Corrected the assignment
        return processInput(userInput),currentScreen
    return currentScreen,needInput
    
    