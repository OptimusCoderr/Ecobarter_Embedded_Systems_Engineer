from os import environ
environ ['PYGAME_HIDE_SUPPORT_PROMPT'] ='1'

import pygame, time
pygame.init()
pygame.mixer.init()

pygame.mixer.set_num_channels(8)
voice = pygame.mixer.Channel(5)


def play_music(file_path):
    try:
        sounda= pygame.mixer.Sound(file_path)
        voice.play(sounda)
              
        # Wait for the music to finish playing
        while voice.get_busy():
            pro_time = time.perf_counter()
        
        # Music finished playing, clean up
       # voice.quit()

    except pygame.error as e:
        print("Pygame error:", e)

    music_file = "Audio/welcome.mp3"

    if __name__ == "__main__":
        play_music(music_file)