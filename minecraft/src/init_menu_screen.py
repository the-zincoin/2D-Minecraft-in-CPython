from pathlib import Path
from file_manager import loadFile
def getCurrentElementData(config,element,init):
    """Äcquires arguments needed for element init class method"""
    offsetsButtons = config.offsets_buttons
    if element["elementType"] == "i": 
        currentElementData = init.inputFieldArgs(element,offsetsButtons,config)   
    else:
        if element["elementType"] == "chab":
            currentElementData = init.chabArgs(element,offsetsButtons,config)  
        else:
            if element["elementType"] == "chob":
                currentElementData = init.chobArgs(element,offsetsButtons,config)
            else:
                currentElementData = init.sliderArgs(element,config,offsetsButtons)
    return currentElementData

def load_menu_screen_metadata():
    """Loads in the menu screen json folders and convert them into a usable dict"""
    base_path = "assets/config/hardcoded/menus/menu_screen_data"
    path_obj = Path(base_path)
    menu_screen_meta_data = {}
    for json_file in path_obj.iterdir():
        file_data = loadFile(json_file.as_posix(),"r")
        menu_screen_meta_data[json_file.name.removesuffix(".json")] = file_data
    return menu_screen_meta_data


def init(config):
    import pygame
    pygame.init()
    pygame.display.set_mode((1, 1))

    from gui_classes import Menu,classManager
    initClassManager = classManager()
    menuscreenData = load_menu_screen_metadata()
    gameMenuScreenData = {}
    for identifier,data in menuscreenData.items():
        menuscreendata = {}
        for element in data["config"]:
            #Possible config statements
            if element["position"][0] == "half":
                element["position"][0] = int(config.length/2)  # Use '=' for assignment
            if element["position"][1] == "half":  # No need for elif; both conditions can be checked independently
                element["position"][1] = int(config.height/2)
            menuscreendata.update(getCurrentElementData(config,element,initClassManager))
        misc_menu_data = data["misc"] #miscallenous data for menu
        #print(misc_menu_data)
        bG = pygame.transform.smoothscale(config.gui_textures["bgAtlas"][misc_menu_data["backGround"]],(2000,1000))
        gameMenuScreenData[identifier] = Menu([menuscreendata,misc_menu_data["text"]],(identifier,bG,misc_menu_data["type"],misc_menu_data["previousScreen"]))
    #print("menuscreendata",gameMenuScreenData)
    return gameMenuScreenData

