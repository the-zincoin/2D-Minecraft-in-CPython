from player import Player
class TerrainState:
    def __init__(self):
        self.terrainStateVariables = {
            "loadedChunks": set(),  #more optmised than lists
            "chunkCache": {},
        }
    
class GameState(Player,TerrainState):
    def __init__(self):
        Player.__init__(self)
        TerrainState.__init__(self)
    