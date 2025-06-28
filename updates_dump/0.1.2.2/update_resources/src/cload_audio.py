import json
import pygame



class Audio_Config_Loader:
    def __init__(self):
        print("Loading Audio...")
        self.load_audio()
        print("Configuring Audio...")
        self.configure_audio()
    def load_audio(self):
        try:
            with open("minecraft/assets/audio/audio.json", "r") as file:
                audio_config = json.load(file)
        except FileNotFoundError:
            print("Error: Audio configuration file not found.")
            return
        #holds the settings for music and sound from audio.json
        self.audio_obj = {
            "menuscreen": {"music": {}, "sound": {}},
            "game": {"music": {}}
        }
        #extracts individual sound elements and chuck into the audio_obj
        for interface_name, audio_dict in audio_config.items():
            for category, audio_list in audio_dict.items():
                for audio_type, audio_path in audio_list.items():
                    file_path = f"minecraft/assets/audio/{audio_path}"
                    self.audio_obj[interface_name][category][audio_type] = pygame.mixer.Sound(file_path)

    def configure_audio(self):
        """Handles the loading of audio metadata."""
        pygame.mixer.init(
            frequency=self.mixer_settings["frequency"],
            size=self.mixer_settings["size"],
            channels=self.mixer_settings["channels"],
            buffer=self.mixer_settings["buffer"]
        )
        self.music_volume_menu = self.interactive_data["settings"]["master_volume"] * self.interactive_data["settings"]["music_volume_menu"]
        self.music_volume_game = self.interactive_data["settings"]["master_volume"] * self.interactive_data["settings"]["music_volume_game"]
        #specific sound elements are chosen.
        self.music_menu = self.audio_obj["menuscreen"]["music"]["main"]
        self.music_menu.set_volume(self.music_volume_menu / 10000)
        self.button_click_sound = self.audio_obj["menuscreen"]["sound"]["buttonClickSound"]
        self.button_click_sound.set_volume(self.mixer_settings["buttonClickVolume"])
        self.music_game = self.audio_obj["game"]["music"]["main"]
        self.music_game.set_volume(self.music_volume_game/10000)