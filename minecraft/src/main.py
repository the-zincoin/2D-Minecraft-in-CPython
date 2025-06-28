# Import necessary modules and files
from init_menu_screen import init
from process_loadsave_inputs import processInput
import pygame
from splash import renderSplash, initSplash
from config_world import Config,processRawGameData, loaded_data,getDateTime
from tile_processor import convertIntoBlocks as cB
from loader_and_saver import saveWorld
from file_manager import loadFile
from perlin_noise_2d import getChunk0Data
from processing_classes import PerlinProperties
import game

pygame.init()

# Initialize window icon and other settings
# Load menu configuration settings
print("Loading Resources. Please Wait...")
menu_default_settings = loadFile("assets/config/hardcoded/menus/menu_settings.json", "r")
atlas_pos = loadFile("assets/textures/gui/menus/menu_elements_metadata/atlas_positions_config.json", "r")
button_sizes = loadFile("assets/config/hardcoded/menus/button_sizes.json", "r")
resource_settings = loadFile("assets/config/hardcoded/game/resource_settings/resource_settings.json", "r")

# Create a configuration object to manage global settings
config = Config(loaded_data["height"], loaded_data["length"], menu_default_settings, atlas_pos,  resource_settings)

# Initialize pygame display settings
pygame.font.init()
pygame.display.set_caption("2D Minecraft v0.1.2 (Official Release Version) Snapshot 1")
font_mojangles_regular = pygame.font.Font("assets/fonts/font_mojangles_regular.otf", round(33 * config.ratio_shrink[1]))

# Configure splash screen and settings
splash_text = initSplash()
config.configure_window(button_sizes)
config.configure_input(font_mojangles_regular, resource_settings["inputField"])
config.configure_slider(resource_settings["slider"]["sliderDim"])
config.configure_splash(len(splash_text), resource_settings["splash"], resource_settings["general"]["shadowBase"])
credits_version_text_colors = resource_settings["general"]["shadowAndTextcolors"]
config.configure_text([tuple(credits_version_text_colors[0]), tuple(credits_version_text_colors[1])])
config.configure_audio(resource_settings["mixer"])
# Set window icon
icon = config.gui_textures["icoAtlas"]["launcherIco"]
pygame.display.set_icon(icon)

# Start playing menu music
config.music_menu.play(-1)

# Load metadata for menu screens
menuscreens_metadata = init(config)
perlin_config = 0

# Initialize screen settings
screen = pygame.display.set_mode((config.length, config.height))
screen_id = "title_screen"
type_interface = "menuscreen"

# Global variables for state management
clock = pygame.time.Clock()
running = True
time_passed = clock.get_time() / 50
checked = False
pressed = False
current_player_x, current_player_y = 0, 0
old_cache_data = ()
game_data = []
raw_game_data = []
world_name, seed = 0, 0
rect = ""
screen_shot_surface = ""
time_since_screen_shot = 0
should_render_debug = resource_settings["general"]["should_render_debug"] != "False"
last_screen_size_refresh = "OFF"
cache_size= 0
chunk_cache_max_size = 0
package_to_cache = 0
def initializeGameData(outcomeFGD):
    """Prepares necessary data for game to commence"""
    global rawGameData,game_data,current_player_x,current_player_y,oldData,world_name,seed,perlin_config,cache_size,chunk_cache_max_size
    rawGameData = processInput(outcomeFGD,config) #processes the game data from the input field values.
    config.interactive_data["settings"]["render_distance"] = rawGameData[2][0]["render_distance"] #sets the settings render distance to the game's render distance to ensure consistent rendering.
    world_name,seed = rawGameData[1],rawGameData[0]
    game_data,chunk_cache_max_size = processRawGameData(rawGameData[2], [],config)
    perlin_config = PerlinProperties(loadFile("assets/config/hardcoded/game/resource_settings/genconsts.json","r"),seed)
    print("PC",perlin_config.genconsts)
    game_data.chunk0Data = cB(getChunk0Data(perlin_config,game_data.seed), 0, game_data)
    current_player_x, current_player_y = game_data.currentPlayerX, game_data.currentPlayerY
    oldData = (_ for _ in game_data.chunkCache.copy().keys()) if game_data.chunkCache else ()
    cache_size = len(tuple(oldData))
# Function to render credits and version information on the title screen
def renderCreditsnVersion():
    for i, surf in enumerate(config.title_text_shadows):
        config.menu_screen_surface.blit(surf, config.title_text_shadow_positions[i])
    for i, surf in enumerate(config.title_text_surfaces):
        config.menu_screen_surface.blit(surf, config.title_text_positions[i])

# Function to handle splash text and special effects
def handleSpecialEffects(screen_id):
    """Blits splash text, credits, and logo on the window"""
    global time_passed
    if screen_id == "title_screen":
        config.menu_screen_surface.blit(config.title_text_logo, config.title_text_logo_rect)
        time_passed += clock.get_time() / 50
        renderSplash(config.menu_screen_surface, "assets/fonts/font_mojangles_regular.otf", splash_text, config.pulse_speed, config.size_range, time_passed, config)
        renderCreditsnVersion()




# Menu screen management functions
def getMenuScreenOutcome(outcome):
    """Handles various outcomes raised by the menu object, such as switching screens or closing the game"""
    global running, screen, screen_id, type_interface
    if outcome == "closed":
        running = False
        pygame.quit()
    elif outcome == "esc":
        screen_id = menuscreens_metadata[screen_id].previousScreen
    elif isinstance(outcome, tuple):
        screen_id = outcome[0]
        return outcome

def handleMenuScreenKeyDown(event):
    """Handles escape key for navigating back to the previous menu"""
    global screen_id
    if event.key == pygame.K_ESCAPE and screen_id != "titleScreen":
        screen_id = menuscreens_metadata[screen_id].previousScreen

def handleMenuScreenOutcome(outcome):
    """Handles changes to settings or inputs in the menu screen"""
    global volume
    if outcome is not None:
        if "world_name" in outcome[1]:
            initializeGameData(outcome[1])
            screen.fill((0, 0, 0))
        elif "master_volume" or "music_volume_menu" or "music_volume_game"in outcome[1]:
            menu_volume = config.interactive_data["settings"]["master_volume"] * config.interactive_data["settings"]["music_volume_menu"]
            game_volume = config.interactive_data["settings"]["master_volume"] * config.interactive_data["settings"]["music_volume_game"]
            config.music_menu.set_volume(menu_volume / 10000)
            config.music_game.set_volume(game_volume/10000)

def runMenuScreen(events,mousePos):
    """Renders and updates the menus"""
    global screen_id, screen,config
    outcome = menuscreens_metadata[screen_id].render(events, config,config.menu_screen_surface,screen,mousePos)
    handleSpecialEffects(screen_id)
    return getMenuScreenOutcome(outcome)






# Game screen management functions
def renderDebug(renderDistance):
    """Displays debugging information on the game screen"""
    playerChunkX = round(current_player_x / game_data.chunkSize)
    playerChunkY = round(current_player_y / game_data.chunkSize)
    debugInfo = (
        "Debug Screen:",
        "2D Minecraft version v0.1.2.SS1 (vanilla)", #modders you can modify this to make it modded
        f"x: {current_player_x:.3f} pixels, {(current_player_x / game_data.tileRes):.3f} blocks, chunkX: {playerChunkX}",
        f"y: {current_player_y:.3f} pixels, {(current_player_y / game_data.tileRes):.3f} blocks, chunkY: {playerChunkY}",
        f"FPS: {int(clock.get_fps())}, MaxFrameRate:{config.interactive_data["settings"]["max_frame_rate"]}",
        f"Seed: {game_data.seed}, RenderDistance: {renderDistance}, Vertical Load Distance: {game_data.rangeY}",
        f"Cached(s): {len(game_data.chunkCache)}, Loaded(s): {len(game_data.loadedChunks)}",
        f"Cached(c): {len(game_data.chunkCache)//game_data.totalYChunks}, Loaded(c): {len(game_data.loadedChunks)//game_data.totalYChunks}",
        f"Tiles rendered: {len(game_data.loadedChunks)*256}",
        f"Buffer Surfaces: {len(game_data.waitListSurfaces)}",
        f"Batched Surfaces: {len(game_data.chunkSurfaces)}"
    )
    for i,line in enumerate(debugInfo):
        renderedText = config.font.render(line, True, (255, 255, 255))
        screen.blit(renderedText, (0, i*36))

def handleGameKeyDownEvent(event):
    """Handles key inputs while ingame"""
    global screen_shot_surface,rect,time_since_screen_shot,should_render_debug
    if event.key == pygame.K_p:
        time = getDateTime()
        screen_shot_surface = font_mojangles_regular.render(f"Screenshot saved at screenshots/Screenshot@{time}.png",True,(255,255,255))
        rect = screen_shot_surface.get_rect(bottomright=(config.length,config.height))
        time_since_screen_shot = pygame.time.get_ticks()
        pygame.image.save(screen,f"screenshots/Screenshot@{time}.png")
    if event.key == pygame.K_d:
        should_render_debug = not should_render_debug

def runINGAMETEXTLine():
    """Renders in game text"""
    global screen_shot_surface,time_since_screen_shot
    if screen_shot_surface != "":
        if (pygame.time.get_ticks()- time_since_screen_shot) > 2000:
            screen_shot_surface = ""
            time_since_screen_shot = pygame.time.get_ticks()
        else:
            screen.blit(screen_shot_surface,rect)
    if should_render_debug:
        renderDebug(config.interactive_data["settings"]["render_distance"])

def runGameScreen(keyPressed):
    """Runs the game itself"""
    global current_player_x, current_player_y,pressed
    pressed, current_player_x, current_player_y = game.run(
        screen, game_data,  pressed, current_player_x, current_player_y, keyPressed, config,perlin_config
    )



#global events


def handleQuit(event):
    global running
    if event.type == pygame.QUIT:
        running = False
        if type_interface == "game":
            saveWorld(world_name, seed, game_data, (current_player_x, current_player_y), set(oldData), config,cache_size,chunk_cache_max_size)

def check_in_full_screen():
    global screen,last_screen_size_refresh
    #print(config.interactiveData["settings"]["full_screen"])
    fullscreen = config.interactive_data["settings"]["full_screen"]
    #print(fullscreen)
    if fullscreen =="ON" and last_screen_size_refresh == "OFF":
        #print(True)
        last_screen_size_refresh = "ON"
        config.scale_screen(config.dimensions[0],config.dimensions[1])
        screen = pygame.display.set_mode((config.length,config.height),pygame.RESIZABLE)
    elif fullscreen == "OFF" and last_screen_size_refresh == "ON":
        #print(True,"off")
        last_screen_size_refresh = "OFF"
        config.scale_screen(loaded_data["length"],loaded_data["height"])
        screen = pygame.display.set_mode((config.length,config.height))

    





def mainGameLoop():
    global running,checked,type_interface,outcome
    while running:
        pygame.display.update()
        check_in_full_screen()
        events = pygame.event.get()
        keyPressed = pygame.key.get_pressed()
        mousePos = pygame.mouse.get_pos()
        relative_mouse_pos = (mousePos[0]/config.offsets_detections[0],mousePos[1]/config.offsets_detections[1])
        if type_interface == "menuscreen" and running:
            outcome = runMenuScreen(events,relative_mouse_pos)
            handleMenuScreenOutcome(outcome)
                
        for event in events:
            handleQuit(event)
            if event.type == pygame.KEYDOWN:
                if type_interface == "menuscreen":
                    handleMenuScreenKeyDown(event)
                else:
                    handleGameKeyDownEvent(event)
        if type_interface == "menuscreen" and running:
            screen.fill((255,255,255))
            screen.blit(pygame.transform.scale(config.menu_screen_surface,config.menu_screen_dim),(0,0))
        
        if screen_id == "game" and running:
            if not checked:
                config.music_menu.stop()
                checked = True
                type_interface = "game"
                config.music_game.play(-1)
            runGameScreen(keyPressed)
            runINGAMETEXTLine()

        if screen_id == "closegame":
            running = False
        clock.tick(config.interactive_data["settings"]["max_frame_rate"])
    print("Closing Resources. Please Wait...")
    pygame.quit()

if __name__=="__main__":
    mainGameLoop() 