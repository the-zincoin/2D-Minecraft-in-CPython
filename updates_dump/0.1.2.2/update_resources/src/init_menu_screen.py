from pathlib import Path
from data_file_manager import loadFile
def getCurrentElementData(resources,element,init):
    """Äcquires arguments needed for element init class method"""
    offsetsButtons = resources.offsets_buttons
    if element["elementType"] == "i": 
        currentElementData = init.inputFieldArgs(element,offsetsButtons,resources)   
    else:
        if element["elementType"] == "chab":
            currentElementData = init.chabArgs(element,offsetsButtons,resources)  
        else:
            if element["elementType"] == "chob":
                currentElementData = init.chobArgs(element,offsetsButtons,resources)
            else:
                currentElementData = init.sliderArgs(element,resources,offsetsButtons)
    return currentElementData

def load_menu_screen_metadata():
    """Loads in the menu screen json folders and convert them into a usable dict"""
    base_path = "minecraft/assets/config/gui/menus/menu_screen_data"
    path_obj = Path(base_path)
    menu_screen_meta_data = {}
    for json_file in path_obj.iterdir():
        file_data = loadFile(json_file.as_posix(),"r")
        menu_screen_meta_data[json_file.name.removesuffix(".json")] = file_data
    return menu_screen_meta_data


def init(resources):
    import pygame

    from menu_manager import Menu,classManager
    initClassManager = classManager()
    menuscreenData = load_menu_screen_metadata()
    gameMenuScreenData = {}
    for identifier,data in menuscreenData.items():
        menuscreendata = {}
        for element in data["config"]:
            menuscreendata.update(getCurrentElementData(resources,element,initClassManager))
        misc_menu_data = data["misc"] #miscallenous data for menu
        #print(misc_menu_data)
        bG = resources.gui_textures["bgAtlas"][misc_menu_data["backGround"]]
        gameMenuScreenData[identifier] = Menu([menuscreendata,misc_menu_data["text"]],(identifier,bG,misc_menu_data["type"],misc_menu_data["previousScreen"]))
    #print("menuscreendata",gameMenuScreenData)
    return gameMenuScreenData

