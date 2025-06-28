import pygame
from rload_button_scaling import scale_button
class Slider:
    def __init__(self, dimensions, resources, text, valueConstraints, textPos, name):
        self.name = name
        self.textPos = textPos
        self.valueConstraints = valueConstraints
        self.divident = dimensions[0] / (valueConstraints[1] - valueConstraints[0])  # Pixels per unit value
        self.offsets = (textPos[0] - dimensions[0] // 2, textPos[0] + dimensions[0] // 2 - 20)  # Slider range
        self.sliderVal = valueConstraints[0]  # Initial value
        self.inInput = False

        # Pre-rendered assets
        self.backGroundSlider = scale_button(resources.button_atlas,dimensions,"unused",resources.border_thickness)
        self.bSRect = self.backGroundSlider.get_rect(center=textPos)
        self.sRect = resources.slider_scaled_states["idle"].get_rect(center=(self.offsets[0] + dimensions[0]//2, textPos[1]))
        self.originalText = text
        self.renderedText = f"{text}: {self.sliderVal}"
        self.type = "s"
        self.defaultValue = resources.interactive_data["settings"][name]
        self.defaultPosSlider = ((self.defaultValue - self.valueConstraints[0]) * self.divident) + self.offsets[0]
        self.sRect.x = self.defaultPosSlider
        self.state = "idle"
    def update(self, args):
        events, bCS,mousepos = args
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    if self.sRect.collidepoint(mousepos):
                        bCS.play()
                        self.state = "hovered"
                        self.inInput = not self.inInput
                    elif self.bSRect.collidepoint(mousepos):
                        bCS.play()
                        self.state = "hovered"
                        self.sRect.x = mousepos[0] - 10
                    else:
                        self.state = "idle"
                        self.inInput = False

        if self.inInput:
            self.sRect.x = mousepos[0] - self.sRect.width // 2

        # Clamp slider position and calculate value
        self.sRect.x = max(self.offsets[0], min(self.sRect.x, self.offsets[1]))
        self.sliderVal = round(((self.sRect.x - self.offsets[0]) / self.divident) + self.valueConstraints[0])
        self.renderedText = f"{self.originalText}: {self.sliderVal}"

    def render(self, args):
        resources = args[1]

        args[0].blit(self.backGroundSlider, self.bSRect)

        # Draw slider button and text

        args[0].blit(resources.slider_scaled_states[self.state], self.sRect)
        textSurf = resources.font.render(self.renderedText, True, (255, 255, 255))
        textShadow = resources.font.render(self.renderedText,True,(50,50,50))
        textShadowrect = textShadow.get_rect(center=(self.textPos[0]+resources.shadow_offsets[0],self.textPos[1]+resources.shadow_offsets[0]))
        textRect = textSurf.get_rect(center=self.textPos)
        args[0].blit(textShadow,textShadowrect)
        args[0].blit(textSurf, textRect)