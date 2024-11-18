from pico2d import *
from character import *

def handle_character_event(character, event):
    if event.type == SDL_KEYDOWN:
        if event.key == SDLK_RIGHT:
            character.velocity = 200
            character.set_action('Run')