# Handles loading of config files
from splash import initSplash
import ast
from data_file_manager import loadFile

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

#Load config Resources
def load_resources():
    print("Loading Resources. Please Wait...")
    loaded_user_settings = load_settings("minecraft/assets/config/settings.txt")
    # Initialize window icon and other settings
    # Load menu configuration settings
    print("Loading Configuration Files...")
    splash_text = initSplash()
    menu_default_settings = loadFile("minecraft/assets/config/gui/menus/menu_settings.json", "r")
    atlas_pos = loadFile("minecraft/assets/textures/gui/menus/menu_elements_metadata/atlas_positions_config.json", "r")
    button_sizes = loadFile("minecraft/assets/config/gui/menus/button_sizes.json", "r")
    resource_settings = loadFile("minecraft/assets/config/game/resource_settings/resource_settings.json", "r")
    return {
        "menu_default_settings":
        menu_default_settings,
        "atlas_position":
        atlas_pos,
        "button_sizes":
        button_sizes,
        "resource_settings":
        resource_settings,
        "loaded_user_settings":
        loaded_user_settings,
        "splash_text":
        splash_text
    }



