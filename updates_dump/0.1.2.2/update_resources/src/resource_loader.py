from data_file_manager import loadFile
from data_file_manager import load_settings
import pygame
pygame.init()
    
# Create a configuration object to manage global settings
# config = Config(loaded_data["height"], loaded_data["length"], menu_default_settings, atlas_pos,  resource_settings)

# # Initialize pygame display settings
# pygame.font.init()
# pygame.display.set_caption("2D Minecraft v0.1.2 (Official Release Version) Snapshot 1")
# font_mojangles_regular = pygame.font.Font("assets/fonts/font_mojangles_regular.otf", round(33 * config.ratio_shrink[1]))

# # Configure splash screen and settings
# splash_text = initSplash()
# config.configure_window(button_sizes)
# config.configure_input(font_mojangles_regular, resource_settings["inputField"])
# config.configure_slider(resource_settings["slider"]["sliderDim"])
# config.configure_splash(len(splash_text), resource_settings["splash"], resource_settings["general"]["shadowBase"])
# credits_version_text_colors = resource_settings["general"]["shadowAndTextcolors"]
# config.configure_text([tuple(credits_version_text_colors[0]), tuple(credits_version_text_colors[1])])
# config.configure_audio(resource_settings["mixer"])