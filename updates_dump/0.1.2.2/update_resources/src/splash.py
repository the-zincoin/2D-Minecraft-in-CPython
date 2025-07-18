import random
def initSplash():
    with open("minecraft/assets/config/gui/menus/splashes.txt","r") as file:
        splashList = list(file.readlines())
        return random.choice(splashList)
def renderSplash(menu_screen_surface,fontName,splash,pulseSpeed,sizeRange,timePassed,resources):
    import math,pygame
    pulse_factor = math.sin(timePassed * pulseSpeed) * 0.5 + 0.5  
    newFontSize = int(sizeRange[0] + (sizeRange[1]-sizeRange[0])* pulse_factor)

    newFont = pygame.font.Font(fontName,newFontSize)
    textsurf = [
        newFont.render(splash, True, (80,80,0)),
        newFont.render(splash, True, (255, 255, 0))
    ]
    pos = resources.splash_position
    for i,surf in enumerate(textsurf):
        surfRotated = pygame.transform.rotate(surf,20)
        surfrect = surfRotated.get_rect(center = pos[i])
        menu_screen_surface.blit(surfRotated,surfrect)
