from WCD import worldData as WD
from WCD import seed,maxFrameRate,currentxpos,currentypos,sky,void,xOffSet
import pygame
import processing as p

run = True

clock = pygame.time.Clock() #clock to track ticks per second
screen = pygame.display.set_mode((WD.length,WD.height-WD.resolutionInTile*2)) #initialize window
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
#creeper icon
icon = pygame.image.load('ImageFiles/Minecraft-creeper-face.jpg')
blockYReference = [[int(y),WD.bottomWrap-y*WD.resolutionInTile] for y in range(0,256)] #acts as a standard y position of 256 for all tiles in all chunks 
pygame.display.set_icon(icon)


pressed = False
def display():
    global yOffSet
    #extract chunk surfaces to blit tiles
    screen.fill((0,0,0))
    for i in range(len(WD.chunkSurfaces)):
        WD.chunkSurfaces[i].fill((0,0,0))



    for i,chunk in enumerate(WD.currentRenderedChunks):
        for x in range(16):
            for y in range(0,WD.verticalNum):
                yrf = blockYReference[y][0]
                block = sky if yrf > 255 else (void if yrf < 0 else (p.checkIfTileLoaded("bedrock.png")  if yrf == 0 else chunk[1][x][255-yrf]))
                #overrides any tile at y=0 into bedrock
                WD.chunkSurfaces[i].blit(block,block.get_rect(midleft=(x*WD.resolutionInTile,blockYReference[y][1]))) #blit tiles on chunk Surface


    #debug
    #print(WD.currentRenderedChunks[0][0],tuple(WD.currentRenderedChunks[0][2]))
    #print(WD.currentRenderedChunks[-1][0],tuple(WD.currentRenderedChunks[-1][2]))
   

    #blit all chunkSurfaces with rendered tiles
    for i,chunk in enumerate(WD.currentRenderedChunks):
        blocksurf = WD.chunkSurfaces[i]
        blockrect = blocksurf.get_rect(midtop = (chunk[2][0],chunk[2][1])) #offset chunk to middle top
        screen.blit(blocksurf,blockrect)
    #debug chunk tiles and borders
    #     screen.set_at(tuple(chunk[2]), (0,255,0))
    #     pygame.draw.line(screen,(255,0,0),(chunk[2][0]-(WD.chunkInPix/2),0),(chunk[2][0]-(WD.chunkInPix/2),350),1)
    #     img = font.render(str(chunk[0]),True,(255,0,0))
    #     screen.blit(img,(chunk[2][0]-(WD.chunkInPix/2),100))
    #for i,block in enumerate(blockYReference):
    #   pygame.draw.line(screen,(255,0,0),(0,block[1]),(length,block[1]),1)


    #render debug line
    img = font.render(f'Debug: x= ({'{:.3f}'.format(-currentxpos)} pixels, {'{:.3f}'.format(-currentxpos/WD.resolutionInTile)} blocks), y=({'{:.3f}'.format(currentypos)} pixels , {'{:.3f}'.format(currentypos/WD.resolutionInTile)} blocks) Fps: {str(int(clock.get_fps()))} Seed: {seed}',True,(255,255,255))
    screen.blit(img,(0,0))
    #debug player position
    #pygame.draw.line(screen,(0,0,255),(length/2,0),(length/2,height),1)
    #pygame.draw.line(screen,(0,0,255),(0,height/2),(length,height/2),1)

#processChunks(-gnum,currentCachenum,-seed)
while run:


    #close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    #get current key pressed
    keyPressed = pygame.key.get_pressed()


    #render and process new and loaded chunks from cache and currentRenderedChunks


    if keyPressed[pygame.K_LEFT]:
        pressed = True
        currentxpos += WD.velocity


        for i,value in enumerate(WD.currentRenderedChunks):
            currChunk = value[2][0]

            if currChunk < WD.rightWrap:
                xOffSet += WD.velocity
                
            else:
                xOffSet = 0-(currChunk-WD.leftWrap) - (WD.rightWrap-currChunk) -WD.chunkInPix + WD.velocity #wraps the new chunk behind the opposite side (chunk clipping)
                p.processNewChunks(-p.gnum,0-seed,value)
            WD.currentRenderedChunks[i][2][0] += xOffSet #change chunks by velocity and whether chunk needs to be wrapped
            xOffSet  = 0



    if keyPressed[pygame.K_RIGHT]:
        pressed = True
        currentxpos -= WD.velocity


        for i,value in enumerate(WD.currentRenderedChunks):
            currChunk = value[2][0]


            if currChunk > WD.leftWrap:
                xOffSet -= WD.velocity


            else:
                xOffSet = (WD.rightWrap - currChunk) +(currChunk-WD.leftWrap)+WD.chunkInPix  - WD.velocity #wraps the new chunk behind the opposite side (chunk clipping)
                p.processNewChunks(p.gnum,seed,value)
            WD.currentRenderedChunks[i][2][0] += xOffSet #change chunks by velocity and whether chunk needs to be wrapped
            xOffSet  = 0



    if keyPressed[pygame.K_UP]:
        pressed = True
        currentypos += WD.velocity



        for i,value in enumerate(blockYReference):
            currTile = value[1]


            if currTile < WD.bottomWrap:
                yOffSet += WD.velocity
                tileLOffset = 0


            else:
                yOffSet = 0-(currTile-WD.topWrap) - (WD.bottomWrap-currTile)  -WD.resolutionInTile+ WD.velocity
                tileLOffset = WD.verticalNum #changes the index of rendering as the new tile displayed is at a different position after being wrapped around (- as you move to before previous index 0)
            blockYReference[i][1] += yOffSet
            blockYReference[i][0] += tileLOffset
            yOffSet = 0



    if keyPressed[pygame.K_DOWN]:
        currentypos -= WD.velocity
        pressed = True


        for i,value in enumerate(blockYReference):
            currTile = value[1]


            if currTile > WD.topWrap:
                yOffSet -= WD.velocity
                tileLOffset = 0


            else:
                yOffSet = (WD.bottomWrap - currTile) +(currTile-WD.topWrap) +WD.resolutionInTile- WD.velocity
                tileLOffset = -WD.verticalNum
            blockYReference[i][1] += yOffSet
            blockYReference[i][0] += tileLOffset #changes the index of rendering as the new tile displayed is at a different position after being wrapped around (+ as you move to after previous index 255)
            yOffSet = 0
    #print(pygame.mouse.get_pos())
    #render chunks and player
    if pressed == True: #ensures that only chunks are re rendered when a key is actually pressed, boosting fps
        display()
        #render player
        surfacePlayer = pygame.surface.Surface((WD.resolutionInTile,WD.resolutionInTile*2))
        surfacePlayer.fill((255,255,255)) #in the future player will be a 2d model instead of a white rectangle
        playerRect = surfacePlayer.get_rect(midtop=(WD.length/2,WD.height/2-WD.resolutionInTile)) #shift player to midtop to look centered and pleasing to look at
        screen.blit(surfacePlayer,playerRect)
        pressed = False
    clock.tick(maxFrameRate) #sets fps/tps
    pygame.display.flip() #update display

pygame.quit()