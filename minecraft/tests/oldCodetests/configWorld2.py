import pygame
from tiles import TileRenderingManager
class MenuscreensConfig:
    def __init__(self):
        self.autoInitMethods = [
            "inputConfig",
            "sliderConfig",
            "splashConfig",
            "titleScreenTextConfig"
            ]
        for method in self.autoInitMethods:
            getattr(self,method)()
    def inputConfig(self):
        self.colorActive = pygame.Color('dodgerblue2')
        self.colorInActive = pygame.Color('lightskyblue3')
        self.cursor = "_"
        self.clickDelay = 300
        self.clickInterval = 50
        self.font = pygame.font.Font("fonts/mojanglesfontRegular.otf",28)
        self.minimumwidth = 350
    def sliderConfig(self):
        self.button = pygame.image.load("textures/originaltextures/button.png")
        self.sliderScaled = pygame.transform.scale(self.button,(20,55))
    def splashConfig(self):
        from splash import initSplash
        self.pulseFactor = 0.5
        self.sizeRange = [31*self.ratioShrink[1]]
        self.sizeRange.append(self.sizeRange[0]+4)
        self.splashText = initSplash()
    def titleScreenTextConfig(self):
        self.textsurf = [self.font.render("2D Minecraft v0.1.2",True,(255,255,255)),self.font.render("All resources belong to Mojang Studios",True,(255,255,255))]
        self.textpos = [self.textsurf[0].get_rect(bottomleft=(0,self.height)),self.textsurf[1].get_rect(bottomright=(self.length,self.height))]
    def renderTitleScreenSpecialEffects(self,screen,timePassed):
        from splash import renderSplash
        renderSplash(screen,"fonts/mojanglesfontRegular.otf",self.splashText,self.pulseFactor,self.sizeRange,timePassed,self.offsetsButtons)
        for i,surf in enumerate(self.textsurf):
            screen.blit(surf,self.textpos[i])


class TerrainConfig:
    def __init__(self):
        self.renderDistance = 1
        self.verticalBlockLoadDistance = 10 #in blocks
        self.scale = 2
        self.numberOfOctaves = 4
        self.loadedChunks = []
        self.seed = 100
        getattr(self,"PerlinConfig")()
        getattr(self,"renderingConfig")()
    #required for perlin Noise to occur
    def PerlinConfig(self):
        self.A =  25214903917
        self.C = 11
        self.M = 2**48
        self.permutationTable = []
        self.gradients = [(1, 1), (-1, 1), (1, -1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
        self.chunkNum = 1
        self.chunkLength = 16
        self.perlinNoiseMap = []
    def renderingConfig(self):
        self.tileRes = 20
        self.chunkSize = self.tileRes * 16
#holds all game related Data


class GameConfig(TerrainConfig,TileRenderingManager):
    def __init__(self):
        TerrainConfig.__init__(self)
        TileRenderingManager.__init__(self)