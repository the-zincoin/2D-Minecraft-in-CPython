import pygame
from numpy import random
from rload_button_scaling import scale_button
from rload_button_scaling import GUI_Button_Scaling as GBS
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
            name: pygame.transform.smoothscale(current_atlas.subsurface(pygame.Rect(element_metadata[0])),element_metadata[1])
            for name, element_metadata in elements.items()
        }
        gui_textures[texture_atlas] = element_dict
    return gui_textures



class GUI_Textures_Text_Loader(GBS):

    # Loads in textures related to the GUIs
    def __init__(self):
        self.menu_screen_surface = pygame.Surface(self.default_screen_dim,pygame.SRCALPHA)

        self.rload_gui_textures()
        print("Loading 9-slice scaler...")
        GBS.__init__(self)
        self.rload_slider()
        self.rload_title_text()


    def rload_gui_textures(self):
        """"Prepare GUI assets"""
        self.gui_textures = prepare_gui_textures(self.atlas_positions)
        self.icon_atlas = self.gui_textures["icoAtlas"]
        self.button_atlas = self.gui_textures["buttons"]
        #print(type[self.button_atlas])
    def rload_slider(self):
        """Prepare slider assets."""
        self.slider_bg = self.gui_textures["buttons"]["unused"] #the states of slider, first preparing base from unused texture, then the hover and idle states for the slider itself.
        #possible states of slider
        slider_states = {
            "idle": self.gui_textures["buttons"]["idle"],
            "hovered": self.gui_textures["buttons"]["hovered"]
        }
        # scaling previous states
        slider_dim = self.slider_settings["sliderDim"]
        self.slider_scaled_states = {
            name: scale_button(self.button_atlas,slider_dim,name,self.border_thickness)
            for name, slider_state in slider_states.items()
        }

    def rload_title_text(self):
        """Configure title text settings."""
        #renders the credits and version...
        text_colors = self.version_display["version_display_metadata"]
        version,credits = self.version_display["version"],self.version_display["credits"]
        self.title_text_surfaces = [
            self.font.render(version, True, text_colors[0]),
            self.font.render(credits, True, text_colors[0])
        ]
        #...and their shadows.
        self.title_text_shadows = [
            self.font.render(version, True, text_colors[1]),
            self.font.render(credits, True, text_colors[1])
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
        self.title_text_logo = self.icon_atlas["minceraftlogo"] if choice == 5783 else self.icon_atlas["minecraftlogo"]
        self.title_text_logo_rect = self.title_text_logo.get_rect(midtop=(self.length // 2, 150))