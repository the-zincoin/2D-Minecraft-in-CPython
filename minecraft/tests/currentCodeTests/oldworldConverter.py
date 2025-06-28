from pathlib import Path
import os
import json,pickle
import shutil
base_path = "WorldSave"
path_obj = Path(base_path)
new_folder = os.makedirs("worlds")
def load_path(path):
    with open(path,"r") as file:
        return json.load(file)
    
def save_path(path,data):
    with open(path,"wb") as file:
        pickle.dump(data,file)
    
for world in path_obj.iterdir():
    game_save_obj = Path(f"{world.as_posix()}/gameSaveData")
    new_world_folder = os.makedirs(f"worlds/{world.as_posix()}")
    for game_save_file in game_save_obj.iterdir():
        if game_save_file.suffix == ".json":
            old_json_data = load_path(game_save_file.as_posix())
            save_path(f"worlds/{world.as_posix()}/gameSaveData",old_json_data)
