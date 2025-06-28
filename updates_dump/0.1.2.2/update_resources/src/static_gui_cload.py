class GUI_Static_Config:
    """Handles static GUI elements."""
    def __init__(self):
        self.configure_splash()
        self.configure_text()

    def configure_splash(self):
        """Display data for splash screens."""
        self.shadow_base = self.general_settings["shadowBase"] #base offset from normal text for shadows
        self.splash_length = len(self.splash_text)
        self.pulse_speed = self.splash_settings["pulseSpeed"] 
        self.splash_shrink = ( #how should the font size shrink or increase based on changes in the user's screen dim settings.
            self.splash_settings["splashBaseCharLength"] / self.splash_length
        ) * self.ratio_shrink[0]
        self.size_range = [ #font size range that changes between screen dims. diff between fonts is an offset applied to make the splash increase and decrease.
            self.splash_settings["baseFontSize"] * self.splash_shrink,
            round(
                self.splash_settings["baseFontSize"] * self.splash_shrink + self.splash_settings["diffBetweenFonts"]
            )
        ]
        self.shadow_offsets.append(self.shadow_base * self.splash_shrink - 1)
        splashBasePos = self.length // 2+930/2, 150+118 #930 and 118 is logo size
        self.splash_position = [ #uses the offsets_buttons variable that changes according to screen dim and shadow_offsets to create shadow
            (splashBasePos[0]-self.offsets_buttons[0]+self.shadow_offsets[1],splashBasePos[1]-self.offsets_buttons[1]+self.shadow_offsets[1]),
            (splashBasePos[0]-self.offsets_buttons[0],splashBasePos[1]-self.offsets_buttons[1])
            ]
    
    def configure_text(self):
        self.credits_text_pos = int(self.length / 2), int(self.height / 2)