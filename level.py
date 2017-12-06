import pygame

from constants import *
from player import Player

class Level:

	def __init__(self, quoteManager):
		self.quoteManager = quoteManager

		self.worldTime = 0

		self.player = Player(quoteManager)

		self.offset = 0
		self.prevOffset = 0

	def tick(self):
		self.worldTime += 1

		self.player.tick()

		self.prevOffset = self.offset
		self.offset += 2.0 + self.worldTime * 0.0005

	def render(self, screen, dt):
		screen.fill(WHITE)

		w = screen.get_width()
		h = screen.get_height()

		pygame.draw.rect(screen, BLACK, (0, h - FLOOR_HEIGHT, w, FLOOR_HEIGHT))
		
		offset = self.prevOffset + (self.offset - self.prevOffset) * dt
		
		self.player.render(screen, dt, offset)