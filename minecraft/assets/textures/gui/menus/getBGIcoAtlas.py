import pygame
pygame.init()
screen = pygame.display.set_mode((1,1))
paths = ("originaltextures/basetextures/ico2dMinecraft.png","originaltextures/basetextures/ico2DMinceraft.png","originaltextures/basetextures/icoLauncher2DMinecraft.png")
sizes = ((468,60),(468,60),(46,46))
atlasSurf = pygame.Surface((512,180),pygame.SRCALPHA)
savePath = "assets/textures/gui/menus/originaltextures/basetextures/icoAtlas.png"
def getBGIcoAtlas(pathArry,imgSizes,atlas,standardSpacing,savePath):
    sizedImgList = []
    for i,path in enumerate(pathArry):
        oImg = pygame.image.load(f"assets/textures/gui/menus/{path}").convert_alpha()
        sizedImg = pygame.transform.scale(oImg,imgSizes[i])
        sizedImgList.append(sizedImg)
    for i,surface in enumerate(sizedImgList):
        atlas.blit(surface,(0,i*standardSpacing))
    pygame.image.save(atlas,savePath)
getBGIcoAtlas(paths,sizes,atlasSurf,60,savePath)