import pygame
from button_class import ButtonChained,ButtonChoice
from rload_button_scaling import scale_button
from input_field_class import InputField
from slider_class import Slider
# Handles menu rendering and processing logic
# Also manages the retrieval of arguments required for running the menus
class handleLiveArg:
    def __init__(self):
        pass

    # Checks the type of interactive element and generates the required arguments for its update and render methods
    def check(self, element, events, resources,time,menu_screen_surface,mousePos):
        if element.type == "i":  # Input field
            args = [(events, time, resources), (menu_screen_surface,resources)]
        elif element.type == "chab":  # Chained action button
            args = [(events, resources.button_click_sound,mousePos), menu_screen_surface]
        elif element.type == "chob":  # Choice button
            args = [(events, resources.button_click_sound,mousePos), (menu_screen_surface,resources)]
        elif element.type == "s":  # Slider
            args = [(events, resources.button_click_sound,mousePos), (menu_screen_surface,resources)]
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
    def renderLogic(self, menu_screen_surface,events, resources, time,mousePos):
        # Draw the background
        menu_screen_surface.fill((0,0,0))
        menu_screen_surface.blit(pygame.transform.scale(self.backGround,(resources.length,resources.height)), (0,0))
        # Render the menu text
        if self.text != "":
            for i, line in enumerate(self.text):
                renderedText = resources.font.render(line, True, (255, 255, 255))
                rect = renderedText.get_rect(center=(resources.credits_text_pos[0],resources.credits_text_pos[1] + i * 36 - 100))
                menu_screen_surface.blit(renderedText, rect)
        # Process interactive elements
        for element in self.menuDataIE.values():
            arguments = args.check(element, events, resources,  time,menu_screen_surface,mousePos)
            outcome = element.update(arguments[0])  # Update the element with relevant arguments
            element.render(arguments[1])  # Render the element
            if outcome is not None:
                if isinstance(outcome, tuple):  # Handle chained elements if needed
                    if outcome[1] != []:
                        args.handleChainedElements(resources.interactive_data, self.menuDataIE, outcome[1])
                return outcome  # Return outcome to handle transitions or updates

    # Handles rendering and logic for hanging menus (blocking flow until resolved)
    def hangingLogic(self,  resources,menu_screen_surface,screen):
        clock = pygame.time.Clock()
        run = True
        while run:
            events = pygame.event.get()
            time = pygame.time.get_ticks()
            mousePos = pygame.mouse.get_pos()
            relative_mouse_pos = (mousePos[0]/resources.offsets_detections[0],mousePos[1]/resources.offsets_detections[1])
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
            outcome = self.renderLogic(menu_screen_surface,events, resources, time,relative_mouse_pos)
            if outcome is not None:
                return outcome
            screen.blit(pygame.transform.scale(menu_screen_surface,resources.menu_screen_dim),(0,0))

            # Update the screen
            pygame.display.update()
            screen.fill((255,255,255))
            clock.tick(60)
    # Entry point for rendering the menu
    def render(self, events, resources,menu_screen_surface,screen,mousePos):
        if self.type == "nh":  # Non-hanging menu
            time = pygame.time.get_ticks()
            return self.renderLogic(menu_screen_surface,events, resources, time,mousePos)
        elif self.type == "h":  # Hanging menu
            return self.hangingLogic(resources,menu_screen_surface,screen)



#handles rendering of sliders that affect setting
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


    def loadButtonStates(self, cache, dimensions, text,resources):
        #print("Resources",resources)
        if text:
            shadow_offset = resources.shadow_offsets[0]
            center_pos = (dimensions[0] // 2, dimensions[1] // 2)
            shadow_pos = (center_pos[0] + shadow_offset, center_pos[1] + shadow_offset) 
            text_surfaces = [
                resources.font.render(text, True, (50, 50, 50)),  # Shadow text
                resources.font.render(text, True, (255, 255, 255))  # Main text  
                ]
            text_rects = [text_surfaces[0].get_rect(center=shadow_pos),text_surfaces[1].get_rect(center=center_pos)]
        else:
            text_surfaces = text_rects = None
        # Process buttons in cache
        states = {}
        for name, button in cache.items():
            # Scale button texture to desired dimensions
            texture = scale_button(resources.button_atlas,dimensions,name,resources.border_thickness)
            # Render text onto the button texture if text is provided
            if text_surfaces and text_rects:
                self.renderButtontext(text_surfaces, text_rects, texture)
            states[name] = texture
        return states
    #ID is the identifier name of all GUI elements (used for menuSettings), whereas text/displayedText is displayed on the GUI element
    #handles init arguments for interactive buttons
    def chabArgs(self,element,offsets,resources):
        sizeButton = resources.button_sizes[element["ID"]]
        #print("ID",element["ID"])
        states = self.loadButtonStates(resources.gui_textures["buttons"],sizeButton,element["displayedText"],resources)
        inst = ButtonChained(states,self.getPos(element["position"],offsets,-1),element["nextScreen"],element["chainedElements"],element["ID"])
        #print("Occured")
        return {element["ID"]:inst}
    

    #handles init arguments for choice buttons
    def chobArgs(self,element,offsets,resources):
        sizeButton = element["size"] #gets size of switchable button
        states = self.loadButtonStates(resources.gui_textures["buttons"],sizeButton,None,resources)
        inst = ButtonChoice(states,self.getPos(element["position"],offsets,-1),element["choices"],element["text"],resources.interactive_data["settings"][element["ID"]])
        return {element["ID"]:inst}
    
    #handles init arguments for input fields
    def inputFieldArgs(self,element,offsets,resources):
        inst = InputField(element["ID"],element["text"],self.getPos(element["position"],offsets,-1),element["size"],resources)
        return {element["ID"]:inst}
    
    #handles init arguments for sliders
    def sliderArgs(self,element,resources,offsets):
        inst = Slider(element["dimensions"],resources,element["text"],element["valueConstraints"],(element["position"][0],element["position"][1]-resources.offsets_buttons[1]),element["ID"])
        return {element["ID"]:inst}
    
    #all init functions return a dictionary of the element's name to the inst of its class containing all information required to render and update the element in the Menu instance

        

