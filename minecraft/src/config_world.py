# Contains World Common Data
import ast
import pygame
import random
import json
from math_dependencies import largest_2_to_1_rectangle
# Initialize pygame
pygame.init()
pygame.font.init()

# Global Variables
loaded_data = {}

# --- Utility Functions ---
def load_settings(filepath):
    """
    Load settings from a text file and parse them into a dictionary.

    Args:
        filepath (str): Path to the settings file.

    Returns:
        dict: Parsed settings data.
    """
    settings = {}
    try:
        with open(filepath, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if ': ' in line and line != lines[0]: #check if the txt line contains settings like length and height
                    key, value = line.split(': ', 1)
                    try:
                        settings[key] = ast.literal_eval(value)
                    except (ValueError, SyntaxError):
                        settings[key] = value
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
    return settings

loaded_data = load_settings("assets/config/settings.txt")


def prepare_gui_textures(atlas_positions, base_path="assets/textures/gui/menus/current_menu_elements/"):
    """
    Prepares GUI textures from the specified atlas positions.

    Args:
        atlas_positions (dict): A dictionary containing atlas names and their element positions.
        base_path (str): Base directory path for texture atlases.

    Returns:
        dict: A dictionary of prepared textures grouped by atlas.
    """
    gui_textures = {}
    for texture_atlas, elements in atlas_positions.items():
        try:
            current_atlas = pygame.image.load(f"{base_path}{texture_atlas}.png") #loads in the current atlas to be extracted
        except pygame.error as e:
            print(f"Error loading texture atlas {texture_atlas}: {e}")
            continue

        element_dict = { #extract each individual element of the atlas and stores it in a dictionary. The atlas's config file is stored in atlasPos.json
            name: current_atlas.subsurface(pygame.Rect(element_pos))
            for name, element_pos in elements.items()
        }
        gui_textures[texture_atlas] = element_dict
    return gui_textures

def calculate_ratio(dim, default_dim):
    """Calculate the scaling ratio based on current and default dimensions."""
    return dim / default_dim

# --- Classes ---
class GUITextures:
    """Handles texture-related operations for GUI elements."""
    def __init__(self, atlas_positions, general_settings):
        self.default_screen_dim = general_settings["defaultScreenDim"] #the default_screen_dim is 2000,1000
        self.general_settings = general_settings #holds general settings held in resource settings.json
        self.ratio_shrink = (
            loaded_data["length"] / general_settings["defaultScreenDim"][0],
            loaded_data["height"] / general_settings["defaultScreenDim"][1]
        ) #scaled elements base on the default settings to the current screen dim.DOES NOT APPLY on full screen mode.
        self.shadow_offsets = [int(general_settings["shadowBase"] * self.ratio_shrink[0])] #shadow_offsets calculated to shrink or increase based on screen dim offset from the default dim.
        self.gui_textures = prepare_gui_textures(atlas_positions)

class GUIInteractiveConfig(GUITextures):
    """Handles interactive GUI elements."""
    def __init__(self, atlas_positions, general_settings):
        super().__init__(atlas_positions, general_settings)

    def configure_input(self, font, input_settings):
        """Configure settings for input fields."""
        self.input_settings = input_settings
        self.color_active = input_settings["colorActive"] #color when input is clicked
        self.color_inactive = input_settings["colorInActive"] #color when input is ignored.
        self.cursor = input_settings["cursor"]
        self.click_delay = input_settings["clickDelay"] #Represents the amount of time required before a continuous backspace is detected
        self.click_interval = input_settings["clickInterval"] #sets how much time between each letter during deletion when continuous backspace occurs
        self.font = font
        self.minimum_width = input_settings["minimumwidth"] #holds base width of input field
        self.char_in_inputfield = input_settings["charInInputfieldbase"] * self.ratio_shrink[0] #Max number of characters that can fit in the input field respective to screen dim and other settings.
        self.additional_metadata = [ #holds data for rendering the credits and version at bottom of screen.
            [self.shadow_offsets[0], self.shadow_offsets[0], tuple(input_settings["shadowAndTextcolors"][0])],
            [0, 0, tuple(input_settings["shadowAndTextcolors"][1])]
        ]

    def configure_slider(self, slider_dim):
        """Prepare slider assets."""
        self.slider_bg = self.gui_textures["buttons"]["unused"] #the states of slider, first preparing base from unused texture, then the hover and idle states for the slider itself.
        slider_states = {
            "idle": self.gui_textures["buttons"]["idle"],
            "hovered": self.gui_textures["buttons"]["hovered"]
        }
        self.slider_scaled_states = {
            name: pygame.transform.scale(slider_state, slider_dim)
            for name, slider_state in slider_states.items()
        }

class GUIStaticConfig:
    """Handles static GUI elements."""
    def __init__(self):
        pass

    def configure_splash(self, splash_length, splash_settings, shadow_base):
        """Display data for splash screens."""
        self.shadow_base = shadow_base #base offset from normal text for shadows
        self.splash_settings = splash_settings
        self.splash_length = splash_length
        self.pulse_speed = splash_settings["pulseSpeed"] 
        self.splash_shrink = ( #how should the font size shrink or increase based on changes in the user's screen dim settings.
            splash_settings["splashBaseCharLength"] / splash_length
        ) * self.ratio_shrink[0]
        self.size_range = [ #font size range that changes between screen dims. diff between fonts is an offset applied to make the splash increase and decrease.
            splash_settings["baseFontSize"] * self.splash_shrink,
            round(
                splash_settings["baseFontSize"] * self.splash_shrink + splash_settings["diffBetweenFonts"]
            )
        ]
        self.shadow_offsets.append(self.shadow_base * self.splash_shrink - 1)
        splashBasePos = self.length // 2+930/2, 150+118 #930 and 118 is logo size
        self.splash_position = [ #uses the offsets_buttons variable that changes according to screen dim and shadow_offsets to create shadow
            (splashBasePos[0]-self.offsets_buttons[0]+self.shadow_offsets[1],splashBasePos[1]-self.offsets_buttons[1]+self.shadow_offsets[1]),
            (splashBasePos[0]-self.offsets_buttons[0],splashBasePos[1]-self.offsets_buttons[1])
            ]
    def configure_text(self, text_colors):
        """Configure title text settings."""
        #renders the credits and version...
        self.title_text_surfaces = [
            self.font.render("2D Minecraft v0.1.2 Snapshot 1", True, text_colors[0]),
            self.font.render("All resources belong to Mojang Studios", True, text_colors[0])
        ]
        #...and their shadows.
        self.title_text_shadows = [
            self.font.render("2D Minecraft v0.1.2 Snapshot 1", True, text_colors[1]),
            self.font.render("All resources belong to Mojang Studios", True, text_colors[1])
        ]
        self.title_text_positions = [
            self.title_text_surfaces[0].get_rect(bottomleft=(0, self.height)),
            self.title_text_surfaces[1].get_rect(bottomright=(self.length, self.height))
        ]
        self.title_text_shadow_positions = [
            self.title_text_surfaces[0].get_rect(bottomleft=(0 + self.shadow_offsets[0], self.height + self.shadow_offsets[0])),
            self.title_text_surfaces[1].get_rect(bottomright=(self.length + self.shadow_offsets[0], self.height + self.shadow_offsets[0]))
        ]
        #picks the minceraft logo or minecraftb logo if the number generator generates a specific number :)
        choice = random.randint(1, 10000)
        self.title_text_logo = pygame.transform.scale(
            self.icon_atlas["minceraftlogo"], (930, 118)
        ) if choice == 5783 else pygame.transform.scale(
            self.icon_atlas["minecraftlogo"], (930, 118)
        )
        self.title_text_logo_rect = self.title_text_logo.get_rect(midtop=(self.length // 2, 150))
        self.credits_text_pos = int(self.length / 2), int(self.height / 2)
class Config(GUIInteractiveConfig, GUIStaticConfig):
    """Child class holding all elements required for the game to run."""
    def __init__(self, height, length, menu_settings, atlas_positions, resource_settings):
        self.height = height
        self.length = length
        self.offsets_buttons = ( #calculated from the ratio between the user's screen dim settings and default screen dim.
            (resource_settings["general"]["defaultScreenDim"][0] - length) / 2,
            (resource_settings["general"]["defaultScreenDim"][1] - height) / 2
        )
        self.interactive_data = menu_settings #acts as a resource location where settings can be modified (type:dict)
        self.music_volume_game = ( 
            self.interactive_data["settings"]["master_volume"] *
            self.interactive_data["settings"]["music_volume_game"]
        )
        self.music_volume_menu = (
            self.interactive_data["settings"]["master_volume"] *
            self.interactive_data["settings"]["music_volume_menu"]
        )
        #initializes the parent classes
        GUIStaticConfig.__init__(self)
        GUIInteractiveConfig.__init__(self, atlas_positions, resource_settings["general"])
        self.menu_screen_surface = pygame.Surface(self.default_screen_dim,pygame.SRCALPHA)
    def configure_window(self,button_sizes):
        self.button_sizes = button_sizes
        self.icon_atlas = self.gui_textures["icoAtlas"]
        monitor_info = pygame.display.Info()
        self.dimensions = (monitor_info.current_w, monitor_info.current_h)
        self.menu_screen_dim = (self.length,self.height) #handles the dimensions of the menu_screen_surface
        self.offsets_detections = (1,1) #handles the offset multiplier to ensure the GUI elements detect the mouse hover
        self.starting_menu_screen_dim = loaded_data #original screen size as per settings

    def configure_audio(self, mixer_settings):
        """Handles the loading of audio metadata."""
        pygame.mixer.init(
            frequency=mixer_settings["frequency"],
            size=mixer_settings["size"],
            channels=mixer_settings["channels"],
            buffer=mixer_settings["buffer"]
        )
        try:
            with open("assets/config/hardcoded/audio.json", "r") as file:
                audio_config = json.load(file)
        except FileNotFoundError:
            print("Error: Audio configuration file not found.")
            return
        #holds the settings for music and sound from audio.json
        self.audio_obj = {
            "menuscreen": {"music": {}, "sound": {}},
            "game": {"music": {}}
        }
        #extracts individual sound elements and chuck into the audio_obj
        for interface_name, audio_dict in audio_config.items():
            for category, audio_list in audio_dict.items():
                for audio_type, audio_path in audio_list.items():
                    file_path = f"assets/audio/{audio_path}"
                    self.audio_obj[interface_name][category][audio_type] = pygame.mixer.Sound(file_path)
        #specific sound elements are chosen.
        self.music_menu = self.audio_obj["menuscreen"]["music"]["main"]
        self.music_menu.set_volume(self.music_volume_menu / 10000)
        self.button_click_sound = self.audio_obj["menuscreen"]["sound"]["buttonClickSound"]
        self.button_click_sound.set_volume(mixer_settings["buttonClickVolume"])
        self.music_game = self.audio_obj["game"]["music"]["main"]
        self.music_game.set_volume(self.music_volume_game/10000)
    #scales screen to full screen mode
    def scale_screen(self,length,height):
        self.length,self.height = length,height
        #finds the largest rectangle capable of fitting in full screen
        self.menu_screen_dim = tuple(largest_2_to_1_rectangle(length,height))
        #print("SC CHECK",self.menu_screen_dim,self.starting_menu_screen_dim)
        self.offsets_detections = self.length/self.starting_menu_screen_dim["length"],self.menu_screen_dim[1]/self.starting_menu_screen_dim["height"] #offsets required for 
        #print(self.offsets_detections)
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