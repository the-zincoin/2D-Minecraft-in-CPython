# Contains World Configuration Classes
import pygame
from interactive_gui_cload import GUI_Interactive_Config as GUIIC
from cload_audio import Audio_Config_Loader as ACL
from rloading_gui_textures import GUI_Textures_Loader as GTL
from static_gui_cload import GUI_Static_Config as GUISC
from cload_window_scale import Window_Scale_Config as WSC
from cload_global import load_resources
# Initialize pygame
pygame.init()
pygame.font.init()


# --- Utility Functions ---

def calculate_ratio(dim, default_dim):
    """Calculate the scaling ratio based on current and default dimensions."""
    return dim / default_dim

# --- Classes ---

class GUI_Resources(GUIIC,GTL,GUISC):
    def __init__(self):
        GTL.__init__(self)
        GUIIC.__init__(self)
        GUISC.__init__(self)


class Config(WSC):

    def __init__(self,resource_settings,menu_settings,button_sizes,atlas_pos,loaded_user_settings):
        self.general_settings = resource_settings["general"]
        self.input_settings = resource_settings["inputField"]
        self.splash_settings = resource_settings["splashSettings"]
        self.mixer_settings = resource_settings["mixer"]
        self.slider_settings = resource_settings["slider"]
        self.interactive_data = menu_settings #acts as a resource location where settings can be modified (type:dict)
        self.atlas_positions = atlas_pos
        self.button_sizes = button_sizes
        self.loaded_user_settings = loaded_user_settings
        WSC.__init__(self)
        ACL.__init__(self)
    


class Resources(GUI_Resources,Config):
    def __init__(self):
        resources = load_resources()
        self.splash_text = resources["splash_text"]
        Config.__init__(self,
                             resources["resource_settings"],
                             resources["menu_settings"],
                             resources["button_sizes"],
                             resources["atlas_position"],
                             resources["loaded_user_settings"])
        GUI_Resources.__init__(self)
        

    
def applyBlur(surf,scalefactor):
    """Blurs a given surface within a factor"""
    width,height = surf.get_size()
    smallImg = pygame.transform.smoothscale(surf,(int(width*scalefactor),int(height*scalefactor)))
    scaledUp = pygame.transform.smoothscale(smallImg,(width,height))
    return scaledUp

    

def prepareX(rD,length):
    """Calculates necessary parameters for tiles on x plane """
    numHorizontalChunks = rD*2+1
    tileRes = int(round(length/(numHorizontalChunks*16))) + 2
    chunkSize = 16 * tileRes
    return numHorizontalChunks,16,tileRes,chunkSize


def prepareY(height,chunkSize,tileRes):
    """Calculates necessary parameters for tiles on y plane """
    rangeY = int(round(round(height/chunkSize) - 1) / 2) + 2
    totalYChunks = rangeY*2+1
    verticalNum = totalYChunks * tileRes 
    return totalYChunks,verticalNum,rangeY


def processRawGameData(gameData,chunk0Data,config):
    """"Prepare data needed for rendering"""
    from processing_classes import renderingWorldClass
    dataX = prepareX(config.interactive_data["settings"]["render_distance"],config.length)
    dataY = prepareY(config.height,dataX[3],dataX[2])
    wrdInit = renderingWorldClass(gameData[0]['chunkCache'],gameData[1],gameData[0]['loadedChunks'])
    wrdInit.processChunks(dataY[1],dataY[2],dataX[0],dataY[0],dataX[2],dataX[3],gameData[0]['seed'],chunk0Data,config.interactive_data["settings"]["velocity"])
    wrdInit.player(gameData[0]['currentPlayerPos'][0],gameData[0]['currentPlayerPos'][1])
    #print(gameData[0]['currentPlayerPos'][0],gameData[0]['currentPlayerPos'][1])
    wrdInit.FOV((config.length//2- dataX[3]/2,config.height //2- dataX[3]/2),dataY[0]/2)
    wrdInit.graphicFiles()
    chunk_cache_max_size = int((config.interactive_data["settings"]["cache_storage_space"]*1024) / (9.5*dataX[0])) #calculates max cache storage in KB (1/1024 MB) and divides by a chunk(9.5 KB per section in total YChunks)
    #print("GD",gameData,type(gameData[0]))
    return wrdInit,chunk_cache_max_size


def getDateTime():
    """Used by screenshot to name screenshot file"""
    from datetime import datetime
    currentTime = datetime.now()
    formattedTime = currentTime.strftime("%Y-%m-%d_%H-%M-%S")
    return formattedTime


currentCachenum = 0
currentTilenum = 0
yOffSet = 0
xOffSet = 0
pygame.quit()