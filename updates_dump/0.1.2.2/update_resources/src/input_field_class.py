import pygame
#handles inputfields
class InputField:
    def __init__(self, name,text, position, size, resources):
        self.name = name
        self.text = ""
        self.rect = pygame.Rect(position[0] - int(resources.minimum_width / 2), position[1], *size)
        self.active = False
        self.color = [50,50,50]
        self.backspaceHeld = False
        self.textHeld = False
        self.indexStart = 0
        self.cursorOn = True
        self.lastBlinkTime = 0
        self.backspaceStartTime = 0
        self.textHeldStartTime = 0
        self.label = resources.font.render(f"{text}: ", True, (255, 255, 255)), \
                     resources.font.render(f"{text}: ", True, (255, 255, 255)).get_rect(topleft=(self.rect.x, self.rect.y - 50))
        self.type = "i"
    def handleEvent(self, event, currentTime, resources):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos[0]/resources.offsets_detections[0],event.pos[1]/resources.offsets_detections[1])
            self.color = resources.color_active if self.active else resources.color_inactive

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
        events,currentTime,resources = args
        for event in events:
            self.handleEvent(event,currentTime,resources)
        if self.backspaceHeld and currentTime - self.backspaceStartTime >= resources.click_delay:
            if (currentTime - self.backspaceStartTime) % resources.click_interval < resources.click_interval / 2:
                self.text = self.text[:-1]

        if currentTime - self.lastBlinkTime >= 400:
            self.cursorOn = not self.cursorOn
            self.lastBlinkTime = currentTime

        self.indexStart = max(0, len(self.text) - 24)

    def render(self, args):
        resources = args[1]
        visibleText = self.text[self.indexStart:self.indexStart + 24]
        if self.active and self.cursorOn:
            visibleText += resources.cursor
        
        

        pygame.draw.rect(args[0], (20, 20, 20), self.rect)
        pygame.draw.rect(args[0], self.color, self.rect, 2)
        args[0].blit(self.label[0], self.label[1])
        for i,metadata in enumerate(resources.additional_metadata):
            txtSurf = resources.font.render(visibleText, True, metadata[2])
            textRect = txtSurf.get_rect(midleft=(self.rect.x + 5+ metadata[0], self.rect.y + self.rect.h // 2+metadata[1]))
            args[0].blit(txtSurf,textRect)