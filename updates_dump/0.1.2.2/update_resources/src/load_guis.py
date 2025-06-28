import pygame
pygame.init()


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



class GUI_Resource_Loader:

    # Loads in textures related to the GUIs
    def __init__(self):
        pass
    def load_gui_textures(self,general_settings,configs):
        self.default_screen_dim = general_settings["defaultScreenDim"] #the default_screen_dim is 2000,1000
        self.general_settings = general_settings #holds general settings held in resource settings.json
        self.ratio_shrink = (
            configs["loaded_data"]["length"] / general_settings["defaultScreenDim"][0],
            configs["loaded_data"]["height"] / general_settings["defaultScreenDim"][1]
        ) #scaled elements base on the default settings to the current screen dim.DOES NOT APPLY on full screen mode.
        self.shadow_offsets = [int(general_settings["shadowBase"] * self.ratio_shrink[0])] #shadow_offsets calculated to shrink or increase based on screen dim offset from the default dim.
        self.gui_textures = prepare_gui_textures(configs["atlas_positions"])