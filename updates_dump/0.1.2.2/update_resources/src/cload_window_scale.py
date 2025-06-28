import pygame
from math_dependencies import largest_2_to_1_rectangle as lgrstRect

class Window_Scale_Config:
    def __init__(self):
        print("Configuring Window Aspects...")
        self.configure_window()
        print("Configuring Scale Attributes...")
        self.configure_scale()
    def configure_window(self):
        
        self.length = self.loaded_user_settings["length"]
        self.height = self.loaded_user_settings["height"]
        
        

        self.default_screen_dim = self.general_settings["defaultScreenDim"] #the default_screen_dim is 2000,1000

        self.starting_menu_screen_dim =  self.loaded_user_settings#original screen size as per settings
        
        self.menu_screen_dim = (self.length,self.height) #handles the dimensions of the menu_screen_surface
    def configure_scale(self):
        self.ratio_shrink = (
            self.starting_menu_screen_dim["length"] / self.general_settings["defaultScreenDim"][0],
            self.starting_menu_screen_dim["height"] / self.general_settings["defaultScreenDim"][1]
        ) #scaled elements base on the default settings to the current screen dim.DOES NOT APPLY on full screen mode.

        self.shadow_offsets = [int(self.general_settings["shadowBase"] * self.ratio_shrink[0])] #shadow_offsets calculated to shrink or increase based on screen dim offset from the default dim.


        self.offsets_buttons = ( #calculated from the ratio between the user's screen dim settings and default screen dim.
            (self.general_settings["defaultScreenDim"][0] - self.length) / 2,
            (self.general_settings["defaultScreenDim"][1] - self.height) / 2
        )

        self.offsets_detections = (1,1)
    #scales screen to full screen mode
    def scale_screen(self,length,height):
        self.length,self.height = length,height
        #finds the largest rectangle capable of fitting in full screen
        self.menu_screen_dim = tuple(lgrstRect(length,height))
        #print("SC CHECK",self.menu_screen_dim,self.starting_menu_screen_dim)
        self.offsets_detections = self.length/self.starting_menu_screen_dim["length"],self.menu_screen_dim[1]/self.starting_menu_screen_dim["height"] #offsets required for 
        #print(self.offsets_detections)
        print("Fullscreendim",self.length,self.height)