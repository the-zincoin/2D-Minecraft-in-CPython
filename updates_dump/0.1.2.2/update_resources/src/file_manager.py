import json,pickle
import pygame,ast
pygame.init()

# Handles loading and unloading of .sav and .json files
def loadFile(path,tag):
    """Loads specified file"""
    with open(path,tag) as file:
        if path.endswith(".json"):
            return json.load(file)
        elif path.endswith(".sav"):
            return pickle.load(file)

def dumpFile(path,data,tag):
    """"Dumps data into specified file"""
    with open(path,tag) as file:
        if path.endswith(".json"):
            json.dump(data,file,indent=4)
        elif path.endswith(".sav"):
            pickle.dump(data,file)

# Handles loading of config files

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

def load_configs():
    loaded_data = load_settings("minecraft/assets/config/settings.txt")
    menu_default_settings = loadFile("minecraft/assets/config/gui/menus/menu_settings.json", "r")
    atlas_pos = loadFile("minecraft/assets/textures/gui/menus/menu_elements_metadata/atlas_positions_config.json", "r")
    button_sizes = loadFile("minecraft/assets/config/gui/menus/button_sizes.json", "r")
    resource_settings = loadFile("minecraft/assets/config/game/resource_settings/resource_settings.json", "r")
    return loaded_data,menu_default_settings,atlas_pos,button_sizes,resource_settings



# Handles loading of image files
def prepare_gui_textures(atlas_positions, base_path="minecraft/assets/textures/gui/menus/current_menu_elements/"):
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



