

def renderChunks(currentPlayerX,currentPlayerY,screen,gameData,config):
    screen.fill((128,188,252))
    renderDistance = config.interactive_data["settings"]["render_distance"]
    #print("Render Distance @ render",renderDistance)
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
        
def run(screen,gameData,pressed,currentPlayerX,currentPlayerY,key,config,perlinConfig):
    from player import renderPlayer
    import chunk_processor as p
    data = p.playerMovement(key,gameData,pressed,currentPlayerX,currentPlayerY,config,perlinConfig)
    coord,pressed = (data[0],data[1]),data[2]
    currentPlayerX,currentPlayerY = coord[0],coord[1]
    if pressed:
        renderChunks(currentPlayerX,currentPlayerY,screen,gameData,config)   
        renderPlayer(screen,gameData.tileRes,config)
        pressed = False
    return pressed,currentPlayerX,currentPlayerY


