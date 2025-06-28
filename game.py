
def renderChunks(currentPlayerX,currentPlayerY,screen,gameData,clock):
    screen.fill((128,188,252))
    gameData.waitListSurfaces.extend([gameData.chunkSurfaces.pop(chunk) for chunk in gameData.chunksToRemove])
    playerChunkX = round(currentPlayerX / gameData.chunkSize)
    playerChunkY = round(currentPlayerY / gameData.chunkSize)
    for xChunk in range(gameData.totalXChunks):
        for yChunk in range(gameData.totalYChunks):
            coord = playerChunkX - gameData.renderDistance +xChunk, playerChunkY - gameData.rangeY+yChunk
            if coord in gameData.loadedChunks.keys():
                Xposition = currentPlayerX-(coord[0]*gameData.chunkSize)+gameData.half[0]
                Yposition = currentPlayerY-(coord[1]*gameData.chunkSize)+gameData.half[1]
                if coord not in gameData.chunkSurfaces:
                    currentData = gameData.loadedChunks[coord].blockData
                    try:        
                        gameData.waitListSurfaces[0].fill((128,188,252)if coord[1] > gameData.checkLength else (0,0,0))
                        for x in range(16):
                            for y in range(16):
                                gameData.waitListSurfaces[0].blit(currentData[x][y],(x*gameData.tileRes,y*gameData.tileRes))
                    except IndexError:
                        gameData.waitListSurfaces[0].fill((0,0,0))

                    gameData.chunkSurfaces[coord] = gameData.waitListSurfaces.pop(0)
                    screen.blit(gameData.chunkSurfaces[coord], (Xposition, Yposition))
                else:
                    screen.blit(gameData.chunkSurfaces[coord],(Xposition,Yposition))   
    img = gameData.fontMojangles.render(
        f'WorldDebug x {'{:.3f}'.format(currentPlayerX)} pixels, {'{:.3f}'.format(currentPlayerX/gameData.tileRes)}blocks, chunkX: {playerChunkX}), {'{:.3f}'.format(currentPlayerY)} pixels , {'{:.3f}'.format(currentPlayerY/(gameData.checkLength)/gameData.tileRes)} blocks, chunkY: {playerChunkY})',True,(255,255,255))
    secondImg = gameData.fontMojangles.render(f'Fps: {str(int(clock.get_fps()))} Seed: {gameData.seed} RenderDistance: {gameData.renderDistance}',True,(255,255,255))
    blitObjects = [(img,(0,0)),(secondImg,(0,50))]
    screen.blits(blitObjects)
def run(screen,gameData,clock,pressed,currentPlayerX,currentPlayerY,key):
    import pygame
    from WCD import length,height
    from FOV import FOV
    from player import renderPlayer
    import processing3 as p
    data = p.playerMovement(key,gameData,pressed,currentPlayerX,currentPlayerY)
    coord,pressed = (data[0],data[1]),data[2]
    currentPlayerX,currentPlayerY = coord[0],coord[1]
    if FOV(key,pygame.time.get_ticks()%2,gameData):
        gameData.updateFOV((length//2- gameData.chunkSize/2,height //2- gameData.chunkSize/2),gameData.totalYChunks/2)
    if pressed:
        renderChunks(currentPlayerX,currentPlayerY,screen,gameData,clock)   
        renderPlayer(screen,gameData.tileRes)
        pressed = False
    return pressed,currentPlayerX,currentPlayerY


