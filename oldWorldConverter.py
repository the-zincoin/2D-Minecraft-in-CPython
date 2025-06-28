from pathlib import Path
import os
import json
import pickle
import shutil


base_path = "WorldSave"
path_obj = Path(base_path)
os.makedirs("worlds")
# Functions to load and save data
def load_path(path):
    with open(path, "r") as file:
        return json.load(file)

def save_path(path, data):
    with open(path, "wb") as file:
        pickle.dump(data, file)

# Iterate through worlds in the WorldSave directory
for world in path_obj.iterdir():
    if world.is_dir():  # Ensure it's a directory
        game_save_obj = world / "gameSaveData"
        
        # Create the corresponding directory in 'worlds'
        new_world_folder = Path(f"worlds/{world.name}")
        os.makedirs(new_world_folder, exist_ok=True)
        if game_save_obj.exists() and game_save_obj.is_dir():
            # Create the gameSaveData directory in the new location
            new_game_save_folder = new_world_folder / "gameSaveData"
            os.makedirs(new_game_save_folder, exist_ok=True)

            for game_save_file in game_save_obj.iterdir():
                if game_save_file.suffix == ".json":
                    old_json_data = load_path(game_save_file)
                    if game_save_file.name == "gameStateData.json":
                        # Replaces old render distance with new
                        render_distance = old_json_data["Render Distance"]
                        del old_json_data["Render Distance"]
                        old_json_data["render_distance"] = render_distance


                    new_file_name = f"{game_save_file.name.removesuffix(".json")}.sav"
                    # Save data in the new location as SAV
                    new_save_path = new_game_save_folder / new_file_name
                    save_path(new_save_path,old_json_data)
        shutil.move(f"WorldSave/{world.name}/chunks",f"worlds/{world.name}")
        shutil.move(f"WorldSave/{world.name}/gameSaveData/waitListSurfaces.png",f"worlds/{world.name}/gameSaveData/waitListSurfaces.png")


