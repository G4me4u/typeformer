import pygame

from constants import *

class QuoteRenderer:

	def __init__(self, quoteManager):
		self.quoteManager = quoteManager

		self.font = pygame.font.SysFont("Courier New", 18)
		
		self.lines = []
		self.renderedLines = []

		self.updateLines()
		self.renderLines()

	def updateLines(self):
		self.rows = []
		
		numQuotes = 0
		leftOver = ""

		rows = 0
		while (True):
			while (len(leftOver) < MAX_WRITING_COLS):
				if (len(leftOver) > 0):
					self.lines.append(leftOver)
				if (numQuotes >= len(self.quoteManager.quotes)):
					leftOver = None
					break
				leftOver = self.quoteManager.getNearbyQuote(numQuotes).text
				numQuotes += 1

			if (not leftOver):
				break

			col = MAX_WRITING_COLS - 1
			while (col > 0 and leftOver[col] != " "):
				col -= 1
			if (col <= 0):
				col = MAX_WRITING_COLS - 1

			self.lines.append(leftOver[:col])
			leftOver = leftOver[col + 1:]
			rows += 1

	def renderLines(self):
		self.renderedLines = []
		for i in range(MAX_WRITING_ROWS):
			self.renderedLines.append(self.font.render(self.lines[i], True, (255, 255, 255)))

	def render(self, screen):
		y = 100
		for line in self.renderedLines:
			screen.blit(line, ((screen.get_width() - line.get_width()) // 2, y))
			y += line.get_height()
