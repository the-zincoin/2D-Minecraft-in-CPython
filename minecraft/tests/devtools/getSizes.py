from pathlib import Path
import pygame,json
pygame.init()
screen = pygame.display.set_mode((1,1))
pathobj = Path("currentWidgets")
widgetsSize  = {}
for file in pathobj.iterdir():
    image = pygame.image.load(file.as_posix()).convert_alpha()
    element = {file.name:image.get_size()}
    widgetsSize.update(element)
with open("sizes.json","w") as file:
    json.dump(widgetsSize,file,indent=4)
