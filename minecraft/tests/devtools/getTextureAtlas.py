from pathlib import Path
import pygame
from math import floor
from loadingImgnJson import dumpFile
pygame.init()

pygame.display.set_mode((50,50))
path = "ImageFilesOld"
output_dir = "textures/blockTextures"
atlas_size = 32
tile_size = 16  




atlas_pixels = atlas_size * tile_size
surf = pygame.Surface((atlas_pixels, atlas_pixels), pygame.SRCALPHA)


fileNamesToPos = {}
index = 0


pathObj = Path(path)
for file in pathObj.iterdir():
    if file.is_file() and file.suffix.lower() == ".png":
        imgFile = pygame.image.load(file.as_posix())
        if imgFile.get_size() == (tile_size, tile_size):
            imgFile = imgFile.convert_alpha()
            x, y = (index % atlas_size) * tile_size, (index // atlas_size) * tile_size
            surf.blit(imgFile, (x, y))
            fileNamesToPos[file.name] = [x, y]
            index += 1


output_path = Path(output_dir) / "blockAtlas.png"
pygame.image.save(surf, output_path.as_posix())
dumpFile("textures/blockMetaData/PNGBlockIdentifier.json",fileNamesToPos,"w")
pygame.quit()



