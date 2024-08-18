import pygame
import os

from sound import Sound
from theme import Theme

class Config :

    def __init__(self) :
        self.themes = []
        self._add_themes()
        self.index = 0
        self.theme = self.themes[self.index]
        # font
        self.font = pygame.font.SysFont('DejaVu Sans', 20, bold=True)
        self.move_sound = Sound(
            os.path.join('Assets/sounds/move.wav'))
        self.capture_sound = Sound(
            os.path.join('Assets/sounds/capture.wav'))

    def change_theme(self) :
        self.index += 1
        self.index %= len(self.themes) # [t1, t2, t3, t4]
        self.theme = self.themes[self.index]

    def _add_themes(self) :
        classic_wood = Theme((222, 184, 135), (139, 69, 19), (255, 228, 181), (160, 82, 45), (255, 239, 213), (210, 105, 30))

        modern_grey = Theme((200, 200, 200), (50, 50, 50), (211, 211, 211), (169, 169, 169), (169, 169, 169), (105, 105, 105))

        oceanic_blue = Theme((173, 216, 230), (0, 105, 148), (175, 238, 238), (70, 130, 180), (135, 206, 250), (25, 25, 112))

        forest_green = Theme((144, 238, 144), (34, 139, 34), (144, 238, 144), (46, 139, 87), (60, 179, 113), (0, 100, 0))

        sunset_orange = Theme((255, 228, 181), (255, 140, 0), (255, 160, 122), (255, 99, 71), (255, 165, 79), (255, 69, 0))

        cool_mint = Theme((152, 255, 152), (0, 128, 128), (175, 238, 238), (32, 178, 170), (144, 238, 144), (0, 139, 139))

        desert_sand = Theme((245, 222, 179), (210, 180, 140), (250, 240, 230), (244, 164, 96), (255, 239, 213), (222, 184, 135))

        self.themes = [classic_wood, modern_grey, oceanic_blue, forest_green, sunset_orange, cool_mint, desert_sand]