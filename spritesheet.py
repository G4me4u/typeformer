import pygame

from constants import *

class SpriteSheet:

	def __init__(self, filepath, tw, th):
		self.filepath = filepath
		self.tw = tw * SPRITE_SCALE
		self.th = th * SPRITE_SCALE

		self.sheet = None

		self.load()

	def load(self):
		sheet = pygame.image.load(self.filepath)
		sheet.convert_alpha()

		w = sheet.get_width()
		h = sheet.get_height()

		self.size = width, height = w * SPRITE_SCALE, h * SPRITE_SCALE
		self.sheet = pygame.transform.scale(sheet, self.size)

	def render(self, screen, x, y, xt, yt):
		x0 = xt * self.tw
		y0 = yt * self.th

		screen.blit(self.sheet, (x, y), area=pygame.Rect(x0, y0, self.tw, self.th))