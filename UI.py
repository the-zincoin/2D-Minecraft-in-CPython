from initMenuScreen import init
import pygame
from initMenuScreen import processInput
from splash import renderSplash,initSplash
from configWorld import Config,loaded_data,processRawGameData,getDateTime
from tileProcessor import convertIntoBlocks as cB
from loaderAndUnloader import loadFile,saveWorld
from Perlin2d import getChunk0Data
import game
pygame.init()
icon = pygame.image.load("textures/widgets/Minecraft-creeper-face.jpg")
mapping = loadFile("config/config.json")
ratioShrink = (loaded_data["length"]/2000),(loaded_data["height"]/1000)
config = Config(loaded_data["height"],loaded_data["length"],mapping,ratioShrink)
music = config.music
pygame.mixer.music.play(-1)
pygame.font.init()
pygame.display.set_icon(icon)
pygame.display.set_caption("2D Minecraft v0.1.2 (Official Release Version)")
fontMojangles = pygame.font.Font("fonts/mojanglesfontRegular.otf", round(33*ratioShrink[1]))
config.inputconfig(fontMojangles)
config.sliderconfig()
config.configureslider()
config.splashConfig()
menuscreensData = init(config)
screen = pygame.display.set_mode((config.length,config.height))
screenID = "titleScreen"
typeInterface = "menuscreen"
clock = pygame.time.Clock()
splashText = initSplash()
running = True
timePassed = clock.get_time() /50
checked = False
pressed = False
currentPlayerX,currentPlayerY = 0,0
oldData = ()
gameData = []
rawGameData = []
worldName,seed = 0,0
textsurf = [config.font.render("2D Minecraft v0.1.2",True,(255,255,255)),config.font.render("All resources belong to Mojang Studios",True,(255,255,255))]
pos = [textsurf[0].get_rect(bottomleft=(0,config.height)),textsurf[1].get_rect(bottomright=(config.length,config.height))]
def handleSpecialEffects(screenID):
    global timePassed
    if screenID == "titleScreen":
        timePassed += clock.get_time() / 50  
        renderSplash(screen,"fonts/mojanglesfontRegular.otf",splashText,config.pulseFactor,config.sizeRange,timePassed,config)
        for i,surf in enumerate(textsurf):
            screen.blit(surf,pos[i])

def handleGameScreen(keyPressed):
    global currentPlayerX, currentPlayerY,pressed
    pressed, currentPlayerX, currentPlayerY = game.run(
        screen, gameData, clock, pressed, currentPlayerX, currentPlayerY, keyPressed, config
    )
def handleTitleScreenEvents(outcome):
    global running,screen,screenID,inOptionsInGame,typeInterface
    if outcome == "closed":
        running = False
        pygame.quit()
    elif outcome == "esc":
        screenID = menuscreensData[screenID].previousScreen
    elif isinstance(outcome,tuple):
        screenID = outcome[0]
        return outcome

def handleTitleScreen(events):
    global screenID,screen
    outcome = menuscreensData[screenID].render(screen,events,config)
    handleSpecialEffects(screenID)
    return handleTitleScreenEvents(outcome)

def initializeGameData(outcomeFGD):
    global rawGameData,gameData,currentPlayerX,currentPlayerY,oldData,worldName,seed
    rawGameData = processInput(outcomeFGD,config)
    config.interactiveData["settings"]["Render Distance"] = rawGameData[2][0]["Render Distance"]
    worldName,seed = rawGameData[1],rawGameData[0]
    gameData = processRawGameData(rawGameData[2], [],config)
    gameData.chunk0Data = cB(getChunk0Data(gameData.seed), 0, gameData)
    currentPlayerX, currentPlayerY = gameData.currentPlayerX, gameData.currentPlayerY
    oldData = (_ for _ in gameData.chunkCache.copy().keys()) if gameData.chunkCache else ()
rect = ""
screenShotsurf = ""
timeSinceScreenShot = 0
while running:
    pygame.display.update()
    events = pygame.event.get()
    keyPressed = pygame.key.get_pressed()
    if typeInterface == "menuscreen":
        outcome = handleTitleScreen(events)
        if outcome is not None:
            if "WorldName" in outcome[1]:
                initializeGameData(outcome[1])
                screen.fill((0,0,0))
            elif "Master Volume" or "Music Volume" in outcome[1]:
                volume = config.interactiveData["settings"]["Master Volume"] * config.interactiveData["settings"]["Music Volume"]
                pygame.mixer.music.set_volume(volume/10000)
            
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            if typeInterface == "game":
                saveWorld(worldName, seed, gameData, (currentPlayerX, currentPlayerY), set(oldData), config)
        if event.type == pygame.KEYDOWN:
                if typeInterface == "menuscreen":
                    if event.key == pygame.K_ESCAPE:
                        if screenID != "titleScreen":
                            screenID = menuscreensData[screenID].previousScreen
                else:
                    if event.key == pygame.K_p:
                        time = getDateTime()
                        screenShotsurf = fontMojangles.render(f"Screenshot saved at screenshots/Screenshot@{time}.png",True,(255,255,255))
                        rect = screenShotsurf.get_rect(bottomright=(config.length,config.height))
                        timeSinceScreenShot = pygame.time.get_ticks()
                        pygame.image.save(screen,f"screenshots/Screenshot@{time}.png")
    
    
    if screenID == "game" and running:
        if not checked:
            checked = True
            typeInterface = "game"
        handleGameScreen(keyPressed)
        if screenShotsurf != "":
            if (pygame.time.get_ticks()- timeSinceScreenShot) > 2000:
                screenShotsurf = ""
                timeSinceScreenShot = pygame.time.get_ticks()
            else:
                screen.blit(screenShotsurf,rect)

    if screenID == "closegame":
        running = False
    clock.tick(config.interactiveData["settings"]["Max Frame Rate"])
pygame.quit()

