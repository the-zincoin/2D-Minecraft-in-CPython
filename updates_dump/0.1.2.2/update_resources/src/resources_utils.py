# Contains World Configuration Classes
import pygame
from interactive_gui_cload import GUI_Interactive_Config as GUIIC
from cload_audio import Audio_Config_Loader as ACL
from rloading_gui_textures_text import GUI_Textures_Text_Loader as GTTL
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

class GUI_Resources(GUIIC,GTTL,GUISC):
    def __init__(self):
        print("Loading GUI Resources...")
        GTTL.__init__(self)
        print("Loading GUI Textures...")
        GUIIC.__init__(self)
        GUISC.__init__(self)
        print("Loading GUI Config...")

class Config(WSC,ACL):

    def __init__(self,resource_settings,menu_settings,button_sizes,atlas_pos,loaded_user_settings):
        # Handle Resource Settings
        print("Loading Global Resource Settings...")
        self.general_settings = resource_settings["general"]
        self.input_settings = resource_settings["input_field"]
        self.splash_settings = resource_settings["splash"]
        self.mixer_settings = resource_settings["mixer"]
        self.slider_settings = resource_settings["slider"]
        self.version_display = resource_settings["version_display"]
        self.slice_scaling_settings = resource_settings["slice_scaling"]

        print("Preparing In-game configurations...")
        self.interactive_data = menu_settings #acts as a resource location where settings can be modified (type:dict)
        self.atlas_positions = atlas_pos #positions of GUI atlases
        self.button_sizes = button_sizes #sizes of buttons 
        self.loaded_user_settings = loaded_user_settings #settings defined by settings.txt

        WSC.__init__(self)
        ACL.__init__(self)
        self.font = pygame.font.Font("minecraft/assets/fonts/font_mojangles_regular.otf", round(self.general_settings["base_font_size"] * self.ratio_shrink[1]))
    


class Resources(GUI_Resources,Config):
    def __init__(self):

        #gets monitor info so that it wont capture screen window size
        monitor_info = pygame.display.Info()
        self.dimensions = (monitor_info.current_w, monitor_info.current_h)

        #Handles resource_screen display
        self.resource_screen_bg = pygame.image.load("minecraft/assets/textures/gui/menus/originaltextures/programmer_art/bgSubMenu.png")
        loading_saving_game_font = pygame.font.Font("minecraft/assets/fonts/font_mojangles_regular.otf",28)

        loading_game_text_surface = loading_saving_game_font.render("Loading Resources. Please Wait...",True,(255,255,255))
        loading_game_text_rect = loading_game_text_surface.get_rect(center=(350,175))

        self.saving_game_text_surface = loading_saving_game_font.render("Saving World...",True,(255,255,255))
        self.closing_resources_text_surface = loading_saving_game_font.render("Closing Resources. Please Wait...",True,(255,255,255))

        resource_screen = pygame.display.set_mode((700, 350))
        resource_screen.blit(self.resource_screen_bg,(0,0))
        resource_screen.blit(loading_game_text_surface,loading_game_text_rect)
        pygame.display.update()



        loaded_resources = load_resources()
        self.splash_text = loaded_resources["splash_text"]
        Config.__init__(self,
                             loaded_resources["resource_settings"],
                             loaded_resources["menu_default_settings"],
                             loaded_resources["button_sizes"],
                             loaded_resources["atlas_position"],
                             loaded_resources["loaded_user_settings"])
        GUI_Resources.__init__(self)
        self.icon = self.gui_textures["icoAtlas"]["launcherIco"]

    
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


def processRawGameData(gameData,chunk0Data,resources):
    """"Prepare data needed for rendering"""
    from processing_classes import renderingWorldClass
    dataX = prepareX(resources.interactive_data["settings"]["render_distance"],resources.length)
    dataY = prepareY(resources.height,dataX[3],dataX[2])
    wrdInit = renderingWorldClass(gameData[0]['chunkCache'],gameData[1],gameData[0]['loadedChunks'])
    wrdInit.processChunks(dataY[1],dataY[2],dataX[0],dataY[0],dataX[2],dataX[3],gameData[0]['seed'],chunk0Data,resources.interactive_data["settings"]["velocity"])
    wrdInit.player(gameData[0]['currentPlayerPos'][0],gameData[0]['currentPlayerPos'][1])
    #print(gameData[0]['currentPlayerPos'][0],gameData[0]['currentPlayerPos'][1])
    wrdInit.FOV((resources.length//2- dataX[3]/2,resources.height //2- dataX[3]/2),dataY[0]/2)
    wrdInit.graphicFiles()
    chunk_cache_max_size = int((resources.interactive_data["settings"]["cache_storage_space"]*1024) / (9.5*dataX[0])) #calculates max cache storage in KB (1/1024 MB) and divides by a chunk(9.5 KB per section in total YChunks)
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