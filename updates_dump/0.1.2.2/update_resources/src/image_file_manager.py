import pygame
pygame.init()

# Handles loading of image files(atlas)
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
