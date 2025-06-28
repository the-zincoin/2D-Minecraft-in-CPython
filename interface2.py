
import pygame
from WCD import length,height
from WCD import processRawGameData
from loadAndUnload import saveWorld
from Perlin2d import getChunk0Data
from tiles2 import convertIntoBlocks as cB
import game,json,startScreen

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((length,height))
titleScreen = pygame.image.load("ImageFiles/TitleScreen.png")
openGameBG = pygame.image.load("ImageFiles/OpenGameBG.png")
buttonOptions = pygame.image.load("ImageFiles/buttonOptions.png").convert_alpha()
buttonOpenGame = pygame.image.load("ImageFiles/buttonOpenGame.png").convert_alpha()
buttonCreateNewWorld = pygame.image.load("ImageFiles/buttonCreateNewWorld.png").convert_alpha()
buttonPlaySelectedWorld = pygame.image.load("ImageFiles/buttonPlaySelectedWorld.png").convert_alpha()
currentPlayerX,currentPlayerY = 0,0
icon = pygame.image.load('ImageFiles/Minecraft-creeper-face.jpg')
caption = pygame.display.set_caption('PaperMinecraftBetav0.1.1 Python')
pygame.display.set_icon(icon)
# Store original button copies
orgButtons = {
    "buttonOptions": buttonOptions.copy(),
    "buttonOpenGame": buttonOpenGame.copy(),
    "buttonCreateNewWorld": buttonCreateNewWorld.copy(),
    "buttonPlaySelectedWorld": buttonPlaySelectedWorld.copy()
}

# Store original screen surfaces
orgScreenSurf = {
    "titleScreen": [titleScreen.copy(),titleScreen.get_rect(center = (length/2,height/2))],
    "openGameBG": [openGameBG.copy(),openGameBG.get_rect(center = (length/2,height/2))]
}

# Define button rectangles with positions
rects = [
    buttonOptions.get_rect(center=(1000,450)),
    buttonOpenGame.get_rect(center=(1000,550)),
    buttonCreateNewWorld.get_rect(center=(800,500)),
    buttonPlaySelectedWorld.get_rect(center=(1200,500))
]
# Load font
fontMojangles = pygame.font.Font("fonts/mojangles.ttf", 28)
with open('PMDataFiles/BlockImagesFull.json', 'r') as file:
    blockImageNames = list(json.load(file))
rectOftile = pygame.Rect(0,0,16,16)

# Define screen states and button configurations
orgScreens = {
    "titleScreen": [
        "titleScreen",
        {
            "b1": [False, rects[0], "buttonOptions", "openGameBg"],
            "b2": [False, rects[1], "buttonOpenGame", "openGameBg"]
        }
    ],
    "openGameBg": [
        "openGameBG",
        {
            "b3": [False, rects[2], "buttonCreateNewWorld", "openGameBgNew"],
            "b4": [False, rects[3], "buttonPlaySelectedWorld", "openGameBgLoad"]
        },
        "titleScreen"
    ],
    "openGameBgLoad": [
        "openGameBG",
        {
            "t1": ["Please type in the name of your world in the Powershell \nPress enter to load world", (350, 500)]
        },
        "openGameBg"
    ],
    "openGameBgNew": [
        "openGameBG",
        {
            "t2": ["Please input the world name and seed in the Powershell \nPress enter to generate world", (400, 500)]
        },
        "openGameBg"
    ],
}
# Define input prompts for specific screens
inputs = {
    "openGameBgLoad": "World name: ",
    "openGameBgNew": "World name and seed (World name, seed): "
}



images = (
     orgScreens,
     orgButtons,
     orgScreenSurf,
     fontMojangles,
     inputs
)
imageAssets = {
    "titleScreen": titleScreen,
    "openGameBG": openGameBG,
    "buttonOptions": buttonOptions,
    "buttonOpenGame": buttonOpenGame,
    "buttonCreateNewWorld": buttonCreateNewWorld,
    "buttonPlaySelectedWorld": buttonPlaySelectedWorld
}

tree = {-2:[("oak_leaves.png",2),("oak_leaves.png",3)],
        -1:[("oak_leaves.png",2),("oak_leaves.png",3),("oak_leaves.png",4),("oak_leaves.png",5)],
        0:[("oak_log.png",0),("oak_log.png",1),("oak_log.png",2),("oak_log.png",3),("oak_leaves.png",4),("oak_leaves.png",5)],
        1:[("oak_leaves.png",2),("oak_leaves.png",3),("oak_leaves.png",4),("oak_leaves.png",5)],
        2:[("oak_leaves.png",2),("oak_leaves.png",3)]}





surf = fontMojangles.render("Saving World...",True,(255,255,255))
run = True
needInput = True
value = None
pressed = False
clock = pygame.time.Clock()
currentScreen = "title"
currentTitleScreen = "titleScreen"
worldName = ""
seed = 0
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            run = False
            if currentScreen == "game":
                screen.fill((0,0,0))
                screen.blit(surf,(0,0))
                pygame.display.update()
                saveWorld(worldName,seed,gameData,(currentPlayerX,currentPlayerY))
    keyPressed = pygame.key.get_pressed()
    if currentScreen == "title":
        value = startScreen.run(screen, currentTitleScreen, needInput, images, imageAssets,events)
        if value is not None:
            if isinstance(value[0], list):
                # Handle game data initialization
                rawGameData = value[0][2]
                gameData = processRawGameData(rawGameData,[],images,imageAssets)
                gameData.chunk0Data = cB(getChunk0Data(gameData.seed), 0, gameData)
                currentPlayerX, currentPlayerY = gameData.currentPlayerX, gameData.currentPlayerY
                worldName,seed = value[0][1],value[0][0]
                currentScreen = value[1]
                screen.fill((0, 0, 0))
            else:
                currentTitleScreen = value[0]
                needInput = value[1]
    elif currentScreen == "game":
        pressed,currentPlayerX,currentPlayerY = game.run(screen,gameData,clock,pressed,currentPlayerX,currentPlayerY,keyPressed)
    clock.tick(60)
    pygame.display.update()
