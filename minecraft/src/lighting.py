import pygame,numpy
maxLightLevel = 15
def enlighten(blockObject,darkeningFactor):
    blockCopy = blockObject.copy()
    blockPixelArray = pygame.surfarray.pixels3d(blockCopy)
    blockPixelArray[:,:,:] = (blockPixelArray[:, :, :] * darkeningFactor).astype(numpy.uint8)
    return pygame.surfarray.make_surface(blockPixelArray)
def getAllLight(blockObject):
    lightLevelsOfBlock = []
    for i in range(maxLightLevel+1):
        try:
            lightLevel = i/maxLightLevel
        except ZeroDivisionError:
            lightLevel = 0
        darkened = enlighten(blockObject,lightLevel)
        lightLevelsOfBlock.append(darkened)
    return list(lightLevelsOfBlock)