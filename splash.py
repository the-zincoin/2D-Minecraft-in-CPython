import random
def initSplash():
    with open("text/splashes.txt","r") as file:
        splashList = list(file.readlines())
        return random.choice(splashList)
def renderSplash(screen,fontName,splash,pulseSpeed,sizeRange,timePassed,config):
    import math,pygame
    offsets=  config.offsetsButtons
    pulse_factor = math.sin(timePassed * pulseSpeed) * 0.5 + 0.5  
    newFontSize = int(sizeRange[0] + (sizeRange[1]-sizeRange[0])* pulse_factor)

    newFont = pygame.font.Font(fontName,newFontSize)
    textsurf = [
        newFont.render(splash, True, (30,30,30)),
        newFont.render(splash, True, (255, 255, 0))
    ]
    pos = [(700-offsets[0]+3,300-offsets[1]+3),(700-offsets[0],300-offsets[1])]
    for i,surf in enumerate(textsurf):
        surfRotated = pygame.transform.rotate(surf,-20)
        surfrect = surfRotated.get_rect(center = pos[i])
        screen.blit(surfRotated,surfrect)
