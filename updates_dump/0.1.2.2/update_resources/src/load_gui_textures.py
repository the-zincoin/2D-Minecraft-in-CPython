import pygame
from file_manager import 
pygame.init()




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