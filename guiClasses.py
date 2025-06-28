import pygame,math
from lighting import enlighten
#handles menu rendering and processing logic
class handleLiveArg:
    def __init__(self):
        pass
    def check(self,element,events,config,screen,time):
        if element.type == "i":
            args = [(events,time,config),(screen,config)]
        elif element.type == "b":
            args = [(events,config.buttonClickSound),screen]
        elif element.type == "s":
            args = [(events,config.buttonClickSound),(screen,config)]
        return args
    def checkReturnVal(self,element):
        if element.type == "i":
            return element.text
        if element.type == "s":
            return element.sliderVal
    def handleChainedElements(self,elementData,menuData,chainedElements):
        for name,ieType in elementData.items():
            for element in ieType.keys():
                if element in chainedElements:
                    elementData[name][element] = self.checkReturnVal(menuData[element])
                    
args = handleLiveArg()
class Menu:
    def __init__(self,menuData,menuConfig):
        self.menuDataIE = menuData[0] #interactiveelements
        self.identifier = menuConfig[0]
        self.backGround = menuConfig[1]
        self.type = menuConfig[2]
        self.previousScreen = menuConfig[3]
        self.text = menuData[1]
    def renderLogic(self,screen,events,config,time):
        screen.fill((0,0,0))
        screen.blit(self.backGround,(-config.offsetsButtons[0],-config.offsetsButtons[1]))
        if self.text != "":
            for i,line in enumerate(self.text):
                renderedText = config.font.render(line, True, (255, 255, 255))
                rect = renderedText.get_rect(center = (int(config.length/2),int(config.height/2)+i*36-100))
                screen.blit(renderedText, rect)
        for element in self.menuDataIE.values():
            arguments = args.check(element,events,config,screen,time)
            outcome = element.update(arguments[0])
            element.render(arguments[1])
            if outcome is not None:
                if isinstance(outcome,tuple):
                    if outcome[1] != []:
                        args.handleChainedElements(config.interactiveData,self.menuDataIE,outcome[1])
                return outcome
    def hangingLogic(self,screen,config):
        clock = pygame.time.Clock()
        run = True
        while run:
            events = pygame.event.get()
            time = pygame.time.get_ticks()
            for event in events:
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    return "closed"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        return "esc"
            outcome = self.renderLogic(screen,events,config,time)
            if outcome is not None:
                return outcome
            pygame.display.update()
            clock.tick(60)

    def render(self,screen,events,config):
        if self.type == "nh":
            time = pygame.time.get_ticks()
            return self.renderLogic(screen,events,config,time)
        elif self.type == "h":
            outcome = self.hangingLogic(screen,config)
            return outcome


            

#handles buttons
class Button:
    def __init__(self,button,Position,nextScreen,chainedElement,name):
        self.name = name
        self.button = button
        self.buttonRect = button.get_rect(center=Position)
        self.nextScreen = nextScreen
        self.type = "b"
        self.chainedElements = chainedElement
        self.borderColor = (0,0,0)
        #iEType #refers to interactive element Type when a button results in interactive elements data being updated like sliders or inputboxes
    def update(self,args):
        events,bCS = args
        for event in events:
            mousePos = pygame.mouse.get_pos()
            if self.buttonRect.collidepoint(mousePos):
                self.borderColor = (255,255,255)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    left, middle, right = pygame.mouse.get_pressed()
                    if left:
                        bCS.play()
                        return (self.nextScreen,self.chainedElements)
            else:
                self.borderColor = (0,0,0)
            
        
    def render(self,screen):
        pygame.draw.rect(self.button,self.borderColor,(0,0,self.buttonRect.width,self.buttonRect.height),3)
        screen.blit(self.button,self.buttonRect)
#handles inputfields
class InputBox:
    def __init__(self, text, position, size, config, name):
        # Initialize the InputBox with essential attributes
        self.name = name  # Name of the input box
        self.text = ""  # Current text inside the input box
        self.rect = pygame.Rect((position[0]-int(config.minimumwidth/2),position[1]), size)  # Rectangular area of the input box
        self.active = False  # Whether the input box is active
        self.backspaceHeld = False  # If backspace key is being held
        self.indexStart = 0  # Index for text scrolling if text exceeds box width
        self.textHeld = False  # If a key for text input is being held
        self.color = pygame.Color('lightskyblue3')  # Default color of the box
        self.backspaceStartTime = 0  # Timestamp for backspace holding
        self.textHeldStartTime = 0  # Timestamp for text holding
        label = config.font.render(f"{text}: ", True, (255, 255, 255))  # Label text for the input box
        self.label = label, label.get_rect(topleft=(self.rect.x, self.rect.y - 50))  # Label text and position
        self.type = "i"  # Type of the input box (default)
        self.cursorOn = True
        self.lastBlinkTime = 0 
    def update(self, args):
        # Update the input box based on events and current time
        events, currentTime, config = args  # Extract arguments (events, time, and config)
        for event in events:
            # Check for mouse click to activate/deactivate the box
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.active = self.rect.collidepoint(event.pos)  # Check if click is within the box
                self.color = config.colorActive if self.active else config.colorInActive  # Change color based on state

            # Handle keypress events if the box is active
            if self.active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:  # Handle backspace key
                    self.text = self.text[:-1]  # Remove last character
                    self.backspaceHeld = True  # Mark backspace as held
                    self.backspaceStartTime = currentTime  # Record the time backspace was pressed
                elif event.key == pygame.K_RETURN:  # Handle Enter key
                    return self.text  # Return the current text
                elif event.unicode:  # Handle any printable character
                    self.text += event.unicode  # Add the character to the text
                    self.textHeld = True  # Mark text input key as held
                    self.textHeldStartTime = currentTime  # Record the time of key press

            # Handle key release events
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE:
                    self.backspaceHeld = False  # Stop backspace holding
                else:
                    self.textHeld = False  # Stop text input key holding

        # Handle repeated backspace when the key is held
        if self.backspaceHeld and currentTime - self.backspaceStartTime >= config.clickDelay:
            if (currentTime - self.backspaceStartTime) % config.clickInterval < config.clickInterval / 2:
                self.text = self.text[:-1]  # Remove character at intervals
        #Handle cursor blink
        if (currentTime - self.lastBlinkTime) >= 400:
            self.cursorOn = not self.cursorOn
            self.lastBlinkTime = currentTime
        # Ensure visible text starts within bounds (for scrolling text)
        self.indexStart = max(0, len(self.text) - 12)
    def render(self, args):
        # Render the input box, label, and text to the screen
        screen, config = args  # Extract screen and config arguments
        
        # Determine visible portion of text and add cursor
        visibleText = self.text[self.indexStart:self.indexStart + 12]
        visibleText += config.cursor if self.cursorOn else ""
        txtSurf = config.font.render(visibleText, True, (255, 255, 255))  # Render the visible text

        # Adjust the input box width to fit the text
        width = max(config.minimumwidth, txtSurf.get_width() + 10)  # Minimum width of 200
        self.rect.w = width  # Update the width of the box

        # Draw the input box background and border
        pygame.draw.rect(screen, (20, 20, 20), self.rect)  # Black background
        pygame.draw.rect(screen, self.color, self.rect, 2)  # Border with active/inactive color

        # Draw the label and the text inside the input box
        screen.blit(self.label[0], self.label[1])  # Render the label
        screen.blit(txtSurf, (self.rect.x + 5, self.rect.y + 5))  # Render the text



class Slider:
    def __init__(self,dimensions,config,text,valueConstraints,textPos,name):
        self.name = name
        start = int(dimensions[0]/2)
        self.offsets = textPos[0]-start,textPos[0]+start - 20 #slider width is width of slider button
        self.backGroundSlider = enlighten(pygame.transform.scale(config.button.copy(),(dimensions)),0.5)
        self.renderedText = ""
        self.originalText = text
        self.bSRect = self.backGroundSlider.get_rect(center = textPos)
        self.sRect = config.sliderScaled.get_rect(center = textPos)
        self.textPos = textPos
        self.valueConstraints = valueConstraints
        self.divident = dimensions[0] / (valueConstraints[1]-valueConstraints[0])  # Total range of values
        self.inInput = False
        self.type = "s"
        self.sliderVal = 0
    def update(self, args):
        events,bCS = args
        mousepos = pygame.mouse.get_pos()
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                left, middle, right = pygame.mouse.get_pressed()
                if left:
                    if self.sRect.collidepoint(mousepos):
                        bCS.play()
                        self.inInput = not self.inInput
                    elif self.bSRect.collidepoint(mousepos):
                        bCS.play()
                        self.sRect.x = mousepos[0] - 10
                    else:
                        self.inInput = False
        if self.inInput:
            self.sRect.x = mousepos[0] - 10

        self.sRect.x = max(self.offsets[0], min(self.sRect.x, self.offsets[1]))
        self.sliderVal = math.ceil(((self.sRect.x-self.offsets[0])/self.divident)+self.valueConstraints[0])
        self.renderedText = f"{self.originalText}: {self.sliderVal}"
    def render(self,args):
        screen,config = args
        pygame.draw.rect(self.backGroundSlider,(0,0,0),(0,0,self.bSRect.width,self.bSRect.height),3)
        screen.blit(self.backGroundSlider,self.bSRect)
        surf = config.font.render(self.renderedText,True,(255,255,255))
        Recttext = surf.get_rect(center=self.textPos)
        screen.blit(config.sliderScaled,self.sRect)
        screen.blit(surf,Recttext)

#handles class initialization
class classManager:
    def __init__(self):
        pass
    def getPos(self,position,offsets,type):
        pos = [
            val + (offsets[i]*type) for i,val in enumerate(position)
        ]
        return pos
    def buttonArgs(self,element,offsets):
        texture = pygame.image.load(f"textures/widgets/{element["path"]}.png").convert_alpha()
        inst = Button(texture,self.getPos(element["position"],offsets,-1),element["nextScreen"],element["chainedElements"],element["path"])
        return {element["path"]:inst}
    def inputBoxArgs(self,element,offsets,config):
        inst = InputBox(element["text"],self.getPos(element["position"],offsets,-1),element["size"],config,element["text"])
        return {element["text"]:inst}
    def sliderArgs(self,element,config,offsets):
        inst = Slider(element["dimensions"],config,element["text"],element["valueConstraints"],(element["position"][0],element["position"][1]-config.offsetsButtons[1]),element["text"])
        return {element["text"]:inst}

        

