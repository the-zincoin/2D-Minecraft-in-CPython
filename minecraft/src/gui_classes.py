import pygame
# Handles menu rendering and processing logic
# Also manages the retrieval of arguments required for running the menus
class handleLiveArg:
    def __init__(self):
        pass

    # Checks the type of interactive element and generates the required arguments for its update and render methods
    def check(self, element, events, config,time,menu_screen_surface,mousePos):
        if element.type == "i":  # Input field
            args = [(events, time, config), (menu_screen_surface,config)]
        elif element.type == "chab":  # Chained action button
            args = [(events, config.button_click_sound,mousePos), menu_screen_surface]
        elif element.type == "chob":  # Choice button
            args = [(events, config.button_click_sound,mousePos), (menu_screen_surface,config)]
        elif element.type == "s":  # Slider
            args = [(events, config.button_click_sound,mousePos), (menu_screen_surface,config)]
        return args

    # Determines the return value for specific interactive element types
    def checkReturnVal(self, element):
        #print("ET",element.type)
        if element.type == "i":
            #print("CRVI",True)
            return element.text  # Text input
        if element.type == "s":
            #print("CRVS",True)
            return element.sliderVal  # Slider value
        if element.type == "chob":
            #print("CRVCHOB",True)
            return element.choices[element.choiceIndex]  # Selected choice

    # Updates elements chained to other elements
    def handleChainedElements(self, elementData, menuData, chainedElements):
        for name, ieType in elementData.items():
            for element in ieType.keys():
                if element in chainedElements:
                    elementData[name][element] = self.checkReturnVal(menuData[element])

# Global instance of handleLiveArg
args = handleLiveArg()


# Handles a singular menu
class Menu:
    def __init__(self, menuData, menuConfig):
        self.menuDataIE = menuData[0]  # Interactive elements of the menu
        self.identifier = menuConfig[0]  # Unique identifier for the menu
        self.backGround = menuConfig[1]  # Background image or texture
        self.type = menuConfig[2]  # Menu type: 'nh' (non-hanging) or 'h' (hanging)
        self.previousScreen = menuConfig[3]  # Reference to the previous screen
        self.text = menuData[1]  # Text displayed on the menu

    # Handles rendering and logic processing for non-hanging menus
    def renderLogic(self, menu_screen_surface,events, config, time,mousePos):
        # Draw the background
        menu_screen_surface.fill((0,0,0))
        menu_screen_surface.blit(pygame.transform.scale(self.backGround,(config.length,config.height)), (0,0))
        # Render the menu text
        if self.text != "":
            for i, line in enumerate(self.text):
                renderedText = config.font.render(line, True, (255, 255, 255))
                rect = renderedText.get_rect(center=(config.credits_text_pos[0],config.credits_text_pos[1] + i * 36 - 100))
                menu_screen_surface.blit(renderedText, rect)
        # Process interactive elements
        for element in self.menuDataIE.values():
            arguments = args.check(element, events, config,  time,menu_screen_surface,mousePos)
            outcome = element.update(arguments[0])  # Update the element with relevant arguments
            element.render(arguments[1])  # Render the element
            if outcome is not None:
                if isinstance(outcome, tuple):  # Handle chained elements if needed
                    if outcome[1] != []:
                        args.handleChainedElements(config.interactive_data, self.menuDataIE, outcome[1])
                return outcome  # Return outcome to handle transitions or updates

    # Handles rendering and logic for hanging menus (blocking flow until resolved)
    def hangingLogic(self,  config,menu_screen_surface,screen):
        clock = pygame.time.Clock()
        run = True
        while run:
            events = pygame.event.get()
            time = pygame.time.get_ticks()
            mousePos = pygame.mouse.get_pos()
            relative_mouse_pos = (mousePos[0]/config.offsets_detections[0],mousePos[1]/config.offsets_detections[1])
            # Handle quit and escape events
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    return "closed"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        return "esc"

            # Render logic for the menu
            outcome = self.renderLogic(menu_screen_surface,events, config, time,relative_mouse_pos)
            if outcome is not None:
                return outcome
            screen.blit(pygame.transform.scale(menu_screen_surface,config.menu_screen_dim),(0,0))

            # Update the screen
            pygame.display.update()
            screen.fill((255,255,255))
            clock.tick(60)
    # Entry point for rendering the menu
    def render(self, events, config,menu_screen_surface,screen,mousePos):
        if self.type == "nh":  # Non-hanging menu
            time = pygame.time.get_ticks()
            return self.renderLogic(menu_screen_surface,events, config, time,mousePos)
        elif self.type == "h":  # Hanging menu
            return self.hangingLogic(config,menu_screen_surface,screen)


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
        config = args[1]
        self.renderBase(args[0])
        txtSurf = config.font.render(self.text,True,(255,255,255))
        txtRect = txtSurf.get_rect(center = self.position)
        txtShadowSurf = config.font.render(self.text,True,(50,50,50))
        txtShadowrect = txtShadowSurf.get_rect(center=(self.position[0]+config.shadow_offsets[0],self.position[1]+config.shadow_offsets[0]))
        args[0].blit(txtShadowSurf,txtShadowrect)
        args[0].blit(txtSurf,txtRect)
        
#Although both classes are similar, they have different purposes as buttons




#handles inputfields
class InputField:
    def __init__(self, name,text, position, size, config):
        self.name = name
        self.text = ""
        self.rect = pygame.Rect(position[0] - int(config.minimum_width / 2), position[1], *size)
        self.active = False
        self.color = [50,50,50]
        self.backspaceHeld = False
        self.textHeld = False
        self.indexStart = 0
        self.cursorOn = True
        self.lastBlinkTime = 0
        self.backspaceStartTime = 0
        self.textHeldStartTime = 0
        self.label = config.font.render(f"{text}: ", True, (255, 255, 255)), \
                     config.font.render(f"{text}: ", True, (255, 255, 255)).get_rect(topleft=(self.rect.x, self.rect.y - 50))
        self.type = "i"
    def handleEvent(self, event, currentTime, config):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos[0]/config.offsets_detections[0],event.pos[1]/config.offsets_detections[1])
            self.color = config.color_active if self.active else config.color_inactive

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.backspaceHeld = True
                self.backspaceStartTime = currentTime
            elif event.key == pygame.K_RETURN:
                return self.text
            elif event.unicode:
                self.text += event.unicode
                self.textHeld = True
                self.textHeldStartTime = currentTime

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_BACKSPACE:
                self.backspaceHeld = False
            else:
                self.textHeld = False

    def update(self, args):
        events,currentTime,config = args
        for event in events:
            self.handleEvent(event,currentTime,config)
        if self.backspaceHeld and currentTime - self.backspaceStartTime >= config.click_delay:
            if (currentTime - self.backspaceStartTime) % config.click_interval < config.click_interval / 2:
                self.text = self.text[:-1]

        if currentTime - self.lastBlinkTime >= 400:
            self.cursorOn = not self.cursorOn
            self.lastBlinkTime = currentTime

        self.indexStart = max(0, len(self.text) - 24)

    def render(self, args):
        config = args[1]
        visibleText = self.text[self.indexStart:self.indexStart + 24]
        if self.active and self.cursorOn:
            visibleText += config.cursor
        
        

        pygame.draw.rect(args[0], (20, 20, 20), self.rect)
        pygame.draw.rect(args[0], self.color, self.rect, 2)
        args[0].blit(self.label[0], self.label[1])
        for i,metadata in enumerate(config.additional_metadata):
            txtSurf = config.font.render(visibleText, True, metadata[2])
            textRect = txtSurf.get_rect(midleft=(self.rect.x + 5+ metadata[0], self.rect.y + self.rect.h // 2+metadata[1]))
            args[0].blit(txtSurf,textRect)

#handles rendering of sliders that affect settings
class Slider:
    def __init__(self, dimensions, config, text, valueConstraints, textPos, name):
        self.name = name
        self.textPos = textPos
        self.valueConstraints = valueConstraints
        self.divident = dimensions[0] / (valueConstraints[1] - valueConstraints[0])  # Pixels per unit value
        self.offsets = (textPos[0] - dimensions[0] // 2, textPos[0] + dimensions[0] // 2 - 20)  # Slider range
        self.sliderVal = valueConstraints[0]  # Initial value
        self.inInput = False

        # Pre-rendered assets
        self.backGroundSlider = pygame.transform.scale(config.gui_textures["buttons"]["unused"],dimensions)
        self.bSRect = self.backGroundSlider.get_rect(center=textPos)
        self.sRect = config.slider_scaled_states["idle"].get_rect(center=(self.offsets[0] + dimensions[0]//2, textPos[1]))
        self.originalText = text
        self.renderedText = f"{text}: {self.sliderVal}"
        self.type = "s"
        self.defaultValue = config.interactive_data["settings"][name]
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
        config = args[1]

        args[0].blit(self.backGroundSlider, self.bSRect)

        # Draw slider button and text

        args[0].blit(config.slider_scaled_states[self.state], self.sRect)
        textSurf = config.font.render(self.renderedText, True, (255, 255, 255))
        textShadow = config.font.render(self.renderedText,True,(50,50,50))
        textShadowrect = textShadow.get_rect(center=(self.textPos[0]+config.shadow_offsets[0],self.textPos[1]+config.shadow_offsets[0]))
        textRect = textSurf.get_rect(center=self.textPos)
        args[0].blit(textShadow,textShadowrect)
        args[0].blit(textSurf, textRect)
#handles class initialization
class classManager:
    def __init__(self):
        pass
    def getPos(self,position,offsets,type):
        pos = [
            val + (offsets[i]*type) for i,val in enumerate(position)
        ]
        return pos
    #Renders the text and shadow of the button on the button using the text and shadow's surfaces and rects


    def renderButtontext(self,textSurf,rects,buttonTexture):
        for i in range(2):
            buttonTexture.blit(textSurf[i],rects[i])
    #loads in button atlas config file from config then scales specifically to the dimensions of the button as stated in atlasPos.json


    def loadButtonStates(self, cache, dimensions, text,config):
        if text:
            shadow_offset = config.shadow_offsets[0]
            center_pos = (dimensions[0] // 2, dimensions[1] // 2)
            shadow_pos = (center_pos[0] + shadow_offset, center_pos[1] + shadow_offset) 
            text_surfaces = [
                config.font.render(text, True, (50, 50, 50)),  # Shadow text
                config.font.render(text, True, (255, 255, 255))  # Main text  
                ]
            text_rects = [text_surfaces[0].get_rect(center=shadow_pos),text_surfaces[1].get_rect(center=center_pos)]
        else:
            text_surfaces = text_rects = None
        # Process buttons in cache
        states = {}
        for name, button in cache.items():
            # Scale button texture to desired dimensions
            texture = pygame.transform.scale(button, dimensions)
            # Render text onto the button texture if text is provided
            if text_surfaces and text_rects:
                self.renderButtontext(text_surfaces, text_rects, texture)
            states[name] = texture
        return states
    #ID is the identifier name of all GUI elements (used for menuSettings), whereas text/displayedText is displayed on the GUI element
    #handles init arguments for interactive buttons
    def chabArgs(self,element,offsets,config):
        sizeButton = config.button_sizes[element["ID"]]
        states = self.loadButtonStates(config.gui_textures["buttons"],sizeButton,element["displayedText"],config)
        inst = ButtonChained(states,self.getPos(element["position"],offsets,-1),element["nextScreen"],element["chainedElements"],element["ID"])
        return {element["ID"]:inst}
    

    #handles init arguments for choice buttons
    def chobArgs(self,element,offsets,config):
        sizeButton = element["size"] #gets size of switchable button
        states = self.loadButtonStates(config.gui_textures["buttons"],sizeButton,None,None)
        inst = ButtonChoice(states,self.getPos(element["position"],offsets,-1),element["choices"],element["text"],config.interactive_data["settings"][element["ID"]])
        return {element["ID"]:inst}
    
    #handles init arguments for input fields
    def inputFieldArgs(self,element,offsets,config):
        inst = InputField(element["ID"],element["text"],self.getPos(element["position"],offsets,-1),element["size"],config)
        return {element["ID"]:inst}
    
    #handles init arguments for sliders
    def sliderArgs(self,element,config,offsets):
        inst = Slider(element["dimensions"],config,element["text"],element["valueConstraints"],(element["position"][0],element["position"][1]-config.offsets_buttons[1]),element["ID"])
        return {element["ID"]:inst}
    
    #all init functions return a dictionary of the element's name to the inst of its class containing all information required to render and update the element in the Menu instance

        

