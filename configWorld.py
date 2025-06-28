

#contains World Common Data
import ast,pygame,random
pygame.init()
pygame.font.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
loaded_data = {}

with open('config/adjustablesettings.txt', 'r') as file:
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

class Config:
    def __init__(self,height,length,mapping,ratioShrink):
        self.height = height
        self.length = length
        self.offsetsButtons = ((2000-length)/2,(1000-height)/2)
        self.ratioShrink = ratioShrink
        self.interactiveData = mapping
        self.music = pygame.mixer.music.load("audio/music/subwoofer_lullaby.mp3")
        self.buttonClickSound = pygame.mixer.Sound("audio/soundeffect/ButtonclickSound.mp3")
        self.buttonClickSound.set_volume(0.5)
    def inputconfig(self,fontMojangles):
        self.colorActive = pygame.Color('dodgerblue2')
        self.colorInActive = pygame.Color('lightskyblue3')
        self.cursor = "_"
        self.clickDelay = 300
        self.clickInterval = 50
        self.font = fontMojangles
        self.minimumwidth = 350
    def sliderconfig(self):
        self.button = pygame.image.load("textures/originaltextures/button.png")
    def configureslider(self):
        self.sliderScaled = pygame.transform.scale(self.button,(20,55))
        pygame.draw.rect(self.sliderScaled,(0,0,0),(0,0,20,55),3)
    def splashConfig(self):
        self.pulseFactor = 0.5
        self.sizeRange = [31*self.ratioShrink[1]]
        self.sizeRange.append(self.sizeRange[0]+4)

def applyBlur(surf,scalefactor):
    width,height = surf.get_size()
    smallImg = pygame.transform.smoothscale(surf,(int(width*scalefactor),int(height*scalefactor)))
    scaledUp = pygame.transform.smoothscale(smallImg,(width,height))
    return scaledUp

    

def prepareX(rD,length):
    numHorizontalChunks = rD*2+1
    tileRes = int(round(length/(numHorizontalChunks*16))) + 2
    chunkSize = 16 * tileRes
    return numHorizontalChunks,16,tileRes,chunkSize


def prepareY(height,chunkSize,tileRes):
    rangeY = int(round(round(height/chunkSize) - 1) / 2) + 2
    totalYChunks = rangeY*2+1
    verticalNum = totalYChunks * tileRes 
    return totalYChunks,verticalNum,rangeY


def processRawGameData(gameData,chunk0Data,config):
    from processingClasses import renderingWorldClass
    print("GD",gameData,type(gameData[0]))
    dataX = prepareX(config.interactiveData["settings"]["Render Distance"],config.length)
    dataY = prepareY(config.height,dataX[3],dataX[2])
    wrdInit = renderingWorldClass(gameData[0]['chunkCache'],gameData[1],gameData[0]['loadedChunks'])
    wrdInit.processChunks(dataY[1],dataY[2],dataX[0],dataY[0],dataX[2],dataX[3],gameData[0]['seed'],chunk0Data,config.interactiveData["settings"]["Max Frame Rate"],config.interactiveData["settings"]["Velocity"])
    wrdInit.player(gameData[0]['currentPlayerPos'][0],gameData[0]['currentPlayerPos'][1])
    wrdInit.FOV((config.length//2- dataX[3]/2,config.height //2- dataX[3]/2),dataY[0]/2)
    wrdInit.graphicFiles()
    return wrdInit


def getDateTime():
    from datetime import datetime
    currentTime = datetime.now()
    formattedTime = currentTime.strftime("%Y-%m-%d_%H-%M-%S")
    return formattedTime


currentCachenum = 0
currentTilenum = 0
yOffSet = 0
xOffSet = 0
pygame.quit()