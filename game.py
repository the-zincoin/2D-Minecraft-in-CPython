
def renderChunks(currentPlayerX,currentPlayerY,screen,gameData,clock,config):
    screen.fill((128,188,252))
    renderDistance = config.interactiveData["settings"]["Render Distance"]
    gameData.waitListSurfaces.extend([gameData.chunkSurfaces.pop(chunk) for chunk in gameData.chunksToRemove])
    playerChunkX = round(currentPlayerX / gameData.chunkSize)
    playerChunkY = round(currentPlayerY / gameData.chunkSize)
    for xChunk in range(gameData.totalXChunks):
        for yChunk in range(gameData.totalYChunks):
            coord = playerChunkX - renderDistance +xChunk, playerChunkY - gameData.rangeY+yChunk
            if coord in gameData.loadedChunks.keys():
                Xposition = currentPlayerX-(coord[0]*gameData.chunkSize)+gameData.half[0]
                Yposition = currentPlayerY-(coord[1]*gameData.chunkSize)+gameData.half[1]
                if coord not in gameData.chunkSurfaces:
                    gameData.loadedChunks[coord].render(gameData,coord)
                    

                    gameData.chunkSurfaces[coord] = gameData.waitListSurfaces.pop(0)
                    screen.blit(gameData.chunkSurfaces[coord], (Xposition, Yposition))
                else:
                    screen.blit(gameData.chunkSurfaces[coord],(Xposition,Yposition))   
    debugInfo = (
        "WorldDebug:",
        f"x={currentPlayerX:.3f} pixels, {currentPlayerX / gameData.tileRes:.3f} blocks, chunkX={playerChunkX}",
        f"y={currentPlayerY:.3f} pixels, {currentPlayerY / (gameData.checkLength * gameData.tileRes):.3f} blocks, chunkY={playerChunkY}",
        f"FPS: {int(clock.get_fps())}, Seed: {gameData.seed}, RenderDistance: {renderDistance}"
    )
    for i,line in enumerate(debugInfo):
        renderedText = config.font.render(line, True, (255, 255, 255))
        screen.blit(renderedText, (0, i*36))
def run(screen,gameData,clock,pressed,currentPlayerX,currentPlayerY,key,config):
    from player import renderPlayer
    import chunkprocessor as p
    data = p.playerMovement(key,gameData,pressed,currentPlayerX,currentPlayerY,config)
    coord,pressed = (data[0],data[1]),data[2]
    currentPlayerX,currentPlayerY = coord[0],coord[1]
    if pressed:
        renderChunks(currentPlayerX,currentPlayerY,screen,gameData,clock,config)   
        renderPlayer(screen,gameData.tileRes,config)
        pressed = False
    return pressed,currentPlayerX,currentPlayerY


