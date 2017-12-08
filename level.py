import pygame

from constants import *
from player import Player
from spritesheet import SpriteSheet

class Level:

	def __init__(self, quoteManager):
		self.quoteManager = quoteManager

		self.worldTime = 0

		self.player = Player(quoteManager)

		self.offset = 0
		self.prevOffset = 0
		self.looseTimer = 1.0

		self.gameOver = False

		self.gameOverFont = pygame.font.SysFont("Courier", 40)
		self.gameOverText = None

		self.background = SpriteSheet(BACKGROUND_SCROLL_PATH, 90, 60)

		self.score = 0

	def reset(self):
		self.offset = 0
		self.prevOffset = 0
		self.worldTime = 0
		self.score = 0
		self.gameOver = False

		self.player.reset()

	def tick(self):
		if (self.gameOver):
			return

		self.worldTime += 1

		self.player.tick()

		self.prevOffset = self.offset
		self.offset += 1.0 + self.worldTime * 0.005

		distAhead = self.player.pos - self.offset
		distRatio = max(min(1.0, 2.0 + distAhead / SCREEN_WIDTH * 4.0), 0.0)
		self.looseTimer = (E ** distRatio - 1.0) / (E - 1.0)

		if (self.looseTimer <= EPSILON):
			self.gameOver = True
			self.gameOverText = self.gameOverFont.render("Game Over", False, WHITE)
			self.scoreText = self.quoteManager.uiFont.render("Score: " + str(int(self.score)), False, WHITE)

		self.score += self.quoteManager.symbolsPerSecond / TPS

	def render(self, screen, dt):
		w = screen.get_width()
		h = screen.get_height()

		if (self.gameOver):
			screen.fill(BLACK)

			xp = (w - self.gameOverText.get_width()) // 2
			yp = (h - self.gameOverText.get_height() - self.scoreText.get_width()) // 2
			screen.blit(self.gameOverText, (xp, yp))

			xp = (w - self.scoreText.get_width()) // 2
			yp += self.gameOverText.get_height()
			screen.blit(self.scoreText, (xp, yp))
			return

		c = 255 * self.looseTimer
		screen.fill((c, c, c))

		c = min(128, 255 - c)
		pygame.draw.rect(screen, (c, c, c), (0, h - FLOOR_HEIGHT, w, FLOOR_HEIGHT))
		
		offset = self.prevOffset + (self.offset - self.prevOffset) * dt
		
		bgw = self.background.tw
		self.background.render(screen, w - ((offset + w) % (bgw * 2)), 0, 0, 0)
		self.background.render(screen, w - ((offset + w - bgw) % (bgw * 2)), 0, 1, 0)

		self.player.render(screen, dt, offset)