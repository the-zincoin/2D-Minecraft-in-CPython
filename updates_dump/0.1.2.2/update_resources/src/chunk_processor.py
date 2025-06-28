from perlin_noise_2d import generatePerlinNoise as gPN
from tile_processor import convertIntoBlocks as cB
from processing_classes import Chunk

# Function to check if a chunk is in the cache, or generate and load it if missing
def checkChunkInCache(coord, gameData, chunkData=[]):
    """
    Checks if a chunk exists in the game data cache.
    If present, retrieves its block data; otherwise, constructs the block data using `chunkData`.
    The chunk is loaded into both `loadedChunks` and `chunkCache`.
    
    Parameters:
        coord: Tuple indicating the (x, y) coordinates of the chunk.
        gameData: Object holding game state, including cached and loaded chunk data.
        chunkData: Pre-generated data for the chunk to be used if it isn't cached.
    """
    if coord in gameData.chunkCache:
        # Retrieve block data from the cached chunk
        blockData = gameData.chunkCache[coord].blockData
    else:
        # Calculate the index within chunk data for proper block assignment
        index = gameData.totalYChunks - (coord[1] + gameData.rangeY)
        blockData = [chunkData[320 * i + index * 16:320 * i + 16 + index * 16] for i in range(16)]
    
    # Load the chunk into active and cached data
    gameData.loadedChunks[coord] = Chunk(True, blockData)
    gameData.chunkCache[coord] = Chunk(False, list(blockData))   

# Function to prepare X-axis tiles for a given chunk
def prepareXTiles(chunkX, side, gameData, perlinConfig):
    """
    Generates a row of tiles along the X-axis using Perlin noise and converts them into blocks.

    Parameters:
        chunkX: X-coordinate of the chunk.
        side: Direction multiplier (-1 for left, 1 for right).
        gameData: Object holding game data, including the seed.
        perlinConfig: Configuration for Perlin noise generation.
    
    Returns:
        List of processed tile data for the specified X-axis chunk.
    """
    dat = list(gPN(256, 3, abs(chunkX) * 16, perlinConfig, gameData.seed * side))[0]
    return cB([dat[15 - n] for n in range(len(dat))] if side == 1 else dat, abs(chunkX), gameData)

# Function to update loaded and cached chunks based on the player's position
def updateChunks(config, gameData, playerX, playerY, perlinConfig):
    """
    Updates the game world by loading new chunks around the player and removing distant chunks.

    Parameters:
        config: Game configuration, including render distance settings.
        gameData: Object holding game data, including chunk cache and loaded chunks.
        playerX, playerY: Current position of the player.
        perlinConfig: Configuration for Perlin noise generation.
    """
    renderDistance = config.interactive_data["settings"]["render_distance"]
    playerChunkX = round(playerX / gameData.chunkSize)
    playerChunkY = round(playerY / gameData.chunkSize)

    # Load chunks within the render distance
    for chunkX in range(-renderDistance, renderDistance + 1):
        currentchunkX = playerChunkX + chunkX
        chunkXdata = prepareXTiles(currentchunkX, -1 if currentchunkX < 0 else 1, gameData, perlinConfig)
        
        for chunkY in range(-gameData.rangeY, gameData.rangeY + 1):
            currentchunkY = playerChunkY + chunkY
            if (currentchunkX, currentchunkY) not in gameData.loadedChunks:
                checkChunkInCache((currentchunkX, currentchunkY), gameData, gameData.chunk0Data if currentchunkX == 0 else chunkXdata)

    # Identify chunks to remove that are outside the render distance
    gameData.chunksToRemove = [
        chunk for chunk in gameData.loadedChunks.keys() 
        if (abs(chunk[0] - playerChunkX) > renderDistance or abs(chunk[1] - playerChunkY) > gameData.rangeY)
    ]

    # Remove the identified chunks and update cache states
    for chunk in gameData.chunksToRemove:
        gameData.chunkCache[chunk].state = False if chunk in gameData.chunkCache else gameData.chunkCache.setdefault(chunk, Chunk(False, gameData.loadedChunks[chunk].blockData))
        del gameData.loadedChunks[chunk]

# Function to handle player movement and trigger chunk updates
def playerMovement(key, gameData, pressed, currentPlayerX, currentPlayerY, config, perlinConfig):
    """
    Handles player movement based on key input and updates the game world accordingly.

    Parameters:
        key: Dictionary of pressed keys.
        gameData: Object holding game state.
        pressed: Boolean indicating if a movement key is pressed.
        currentPlayerX, currentPlayerY: Current position of the player.
        config: Game configuration, including settings for chunk updates.
        perlinConfig: Configuration for Perlin noise generation.
    
    Returns:
        Updated player position and movement state.
    """
    import pygame
    velocity = gameData.velocity
    if key[pygame.K_RIGHT]:
        currentPlayerX -= velocity  # Move player right
        pressed = True
    elif key[pygame.K_LEFT]:
        currentPlayerX += velocity  # Move player left
        pressed = True
    elif key[pygame.K_UP]:
        currentPlayerY += velocity  # Move player up
        pressed = True
    elif key[pygame.K_DOWN]:
        currentPlayerY -= velocity  # Move player down
        pressed = True

    # If the player moved, update loaded chunks
    if pressed:
        updateChunks(config, gameData, currentPlayerX, currentPlayerY, perlinConfig)
    return currentPlayerX, currentPlayerY, pressed




