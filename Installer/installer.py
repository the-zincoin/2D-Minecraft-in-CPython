import os
import shutil
from win32com.client import Dispatch

def create_shortcut(target, shortcut_path, description=None, icon=None):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortcut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    if description:
        shortcut.Description = description
    if icon:
        shortcut.IconLocation = icon
    shortcut.save()

def install_game():
    game_folder = r"C:\Users\Matthew/OneDrive\Documents\2DMinecraftPack"
    target_path = os.path.join(game_folder, "game.exe")
    icon_file = os.path.join(game_folder, "icon.ico")
    
    # Ensure the folder exists
    if not os.path.exists(game_folder):
        os.makedirs(game_folder)

    # Copy game files to the Program Files folder
    shutil.copy(os.path.join('2DMinecraftPack/Game', 'game.exe'), game_folder)
    shutil.copy(os.path.join('2DMinecraftPack/Game', 'icon2dmc.ico'), game_folder)

    # Create a desktop shortcut
    desktop_shortcut = os.path.join(os.environ["USERPROFILE"], "2DMinecraftPack/Shortcuts", "2DMinecraftShortcut.lnk")
    create_shortcut(target_path, desktop_shortcut, description="Play 2D Minecraft", icon=icon_file)
    
    print("Installation complete and shortcut created on Desktop.")

if __name__ == "__main__":
    install_game()