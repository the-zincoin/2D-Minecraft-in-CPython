import os
from check_path_Walker import find_file_in_directory as ffid
import win32com.client

def create_shortcut(exe_path, icon_path, game_name):
    # Get the Desktop directory path
    start_menu_path = os.path.join(os.environ["USERPROFILE"], "Start Menu")
    shortcut_path = os.path.join(start_menu_path, f'{game_name}.lnk')  # Save to Start Menu

    # Create a shortcut using COM
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    
    # Set shortcut properties
    shortcut.TargetPath = exe_path
    shortcut.WorkingDirectory = os.path.dirname(exe_path)
    shortcut.IconLocation = icon_path
    shortcut.save()

    print(f'Shortcut created at {shortcut_path}')

# Replace with the path to your .exe and .ico files
game_name = "2D Minecraft v0.1.2"
base_path = ffid("game.exe","minecraft")
exe_file = fr'{base_path}\game.exe'
icon_file = fr'{base_path}\icon2dmc.ico'



create_shortcut(exe_file, icon_file, game_name)