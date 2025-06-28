import pygame
class GUI_Interactive_Config:
    """Handles interactive GUI elements."""
    def __init__(self):
        self.configure_input()
    def configure_input(self):
        """Configure settings for input fields."""

        self.color_active = self.input_settings["colorActive"] #color when input is clicked
        self.color_inactive = self.input_settings["colorInActive"] #color when input is ignored.

        self.cursor = self.input_settings["cursor"]

        self.click_delay = self.input_settings["clickDelay"] #Represents the amount of time required before a continuous backspace is detected
        self.click_interval = self.input_settings["clickInterval"] #sets how much time between each letter during deletion when continuous backspace occurs

        self.minimum_width = self.input_settings["minimumwidth"] #holds base width of input field
        self.char_in_inputfield = self.input_settings["charInInputfieldbase"] * self.ratio_shrink[0] #Max number of characters that can fit in the input field respective to screen dim and other settings.


        self.additional_metadata = [ #holds data for rendering the credits and version at bottom of screen.
            [self.shadow_offsets[0], self.shadow_offsets[0], tuple(self.input_settings["input_field_text_metadata"][0])],
            [0, 0, tuple(self.input_settings["input_field_text_metadata"][1])]
        ]