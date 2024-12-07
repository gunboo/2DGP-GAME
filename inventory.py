from pico2d import *
from character import Character
class Inventory:
    def __init__(self, character):
        self.character = character
        self.ui_image = load_image('potion_ui.png')
        self.hp_potion_image = load_image('hp_potion.png')
        self.mp_potion_image = load_image('mp_potion.png')
        self.hp_potion_count = 100
        self.mp_potion_count = 100
        self.ui_x, self.ui_y = 300, 560

    def draw(self):
        self.ui_image.draw(self.ui_x, self.ui_y)

        self.hp_potion_image.draw(336, 580)
        self.mp_potion_image.draw(336, 545)

    def update(self):
       pass
