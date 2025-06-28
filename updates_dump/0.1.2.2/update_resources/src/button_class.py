import pygame
# Represents a basic button with multiple states
class Button:
    def __init__(self, position, name, states):
        self.name = name  # Button name
        self.position = position  # Button position
        self.buttonRect = states["idle"].get_rect(center=position)
        self.currentState = "idle"  # Display state: idle or hovered
        self.states = states  # All available states

    # Handles hover and click events for the button
    def handleHover(self, events, bCS,mousePos):
        isHovered = self.buttonRect.collidepoint(mousePos)
        self.currentState = "hovered" if isHovered else "idle"

        # Handle button clicks
        for event in events:
            if isHovered and event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:  # Left-click
                bCS.play()  # Play button click sound
                return True

    # Renders the button to the screen
    def renderBase(self, menu_screen_surface):
        menu_screen_surface.blit(self.states[self.currentState], self.buttonRect)


# Chained button that performs actions like switching screens or saving data
class ButtonChained(Button):
    def __init__(self, states, position, nextScreen, chainedElements, name):
        Button.__init__(self, position, name, states)
        self.nextScreen = nextScreen  # The next screen to transition to
        self.type = "chab"  # Button type: chained action button
        self.chainedElements = chainedElements  # Elements to update as a result of interaction

    # Updates the button state and returns the next screen and chained elements
    def update(self, args):
        events, bCS,mousePos = args
        outcome = self.handleHover(events, bCS,mousePos)
        if outcome is not None:
            return self.nextScreen, self.chainedElements

    # Renders the button
    def render(self, menu_screen_surface):
        self.renderBase(menu_screen_surface)

class ButtonChoice(Button): #has actions related to adjusting settings which lead to outcomes
    def __init__(self, states,position,choices,name,defindex):
        Button.__init__(self,position,name,states)
        self.type = "chob"
        self.choiceIndex = defindex
        self.choices = choices
        self.wrap = len(self.choices)
        self.text = f"{self.name}: {self.choices[self.choiceIndex]}"
    def update(self,args):
        events,bCS,mousePos = args
        outcome = self.handleHover(events,bCS,mousePos)
        if outcome is not None:
            #print("CI",True)
            self.choiceIndex = (self.choiceIndex + 1) % self.wrap
            self.text = f"{self.name}: {self.choices[self.choiceIndex]}"
    def render(self,args):
        resources = args[1]
        self.renderBase(args[0])
        txtSurf = resources.font.render(self.text,True,(255,255,255))
        txtRect = txtSurf.get_rect(center = self.position)
        txtShadowSurf = resources.font.render(self.text,True,(50,50,50))
        txtShadowrect = txtShadowSurf.get_rect(center=(self.position[0]+resources.shadow_offsets[0],self.position[1]+resources.shadow_offsets[0]))
        args[0].blit(txtShadowSurf,txtShadowrect)
        args[0].blit(txtSurf,txtRect)
        
#Although both classes are similar, they have different purposes as buttons