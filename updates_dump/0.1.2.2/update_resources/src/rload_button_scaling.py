import pygame
def scale_button(button_atlas,element_dim,type,border_thickness):
        #prepare resources
        new_button_surface = pygame.Surface(tuple(element_dim)) #surface for scaled button
        sections = button_atlas[type] #specific button type


        #calculation variables
        border_thickness2 = border_thickness*2


        #scale middle section
        middle_section = sections["middle_section"]
        new_button_surface.blit(pygame.transform.scale(middle_section,(element_dim[0]-border_thickness2,element_dim[1]-border_thickness2)),(border_thickness,border_thickness))

        #scale and blit each slice
        new_button_surface.blit(pygame.transform.scale(sections["top_section"],(element_dim[0]-border_thickness2,border_thickness)),(border_thickness,0))
        new_button_surface.blit(pygame.transform.scale(sections["bottom_section"],(element_dim[0]-border_thickness2,border_thickness)),(border_thickness,element_dim[1]-border_thickness))
        new_button_surface.blit(pygame.transform.scale(sections["left_section"],(border_thickness,element_dim[1])),(0,0))
        new_button_surface.blit(pygame.transform.scale(sections["right_section"],(border_thickness,element_dim[1])),(element_dim[0]-border_thickness,0))
        

        return new_button_surface

class GUI_Button_Scaling:
    def __init__(self):
        self.prepare_scaling_rects()
        self.prepare_scaling_assets()
    def prepare_scaling_rects(self):

        self.scaling_rects = {}
        for section,rect in self.slice_scaling_settings["sections"].items():
            self.scaling_rects[section] = pygame.Rect(rect[0],rect[1],rect[2],rect[3])

    def prepare_scaling_assets(self):
        #Iterates through each type of button
        self.border_thickness = self.slice_scaling_settings["border_thickness"]
        for button_type,button_texture in self.button_atlas.items():
            button_scaled_slices = {}
            for section,rect in self.scaling_rects.items():
                #Obtain the slices
                section_texture = button_texture.subsurface(rect)
                button_scaled_slices[section] = section_texture
            #update original texture
            self.button_atlas[button_type] = button_scaled_slices
        #print("BA",self.button_atlas)



