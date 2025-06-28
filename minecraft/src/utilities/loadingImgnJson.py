import json,pygame
def openFile(path):
    with open(path,"r") as file:
        return json.load(file)
def dumpFile(path,data,tag):
    with open(path,tag) as file:
        json.dump(data,file,indent=4)
def loadImage(path):
    return pygame.image.load(path).convert_alpha()
