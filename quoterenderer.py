import pygame

from constants import *

from quoteline import QuoteLine

class QuoteRenderer:

	def __init__(self, quoteManager):
		self.quoteManager = quoteManager

		self.textFont = pygame.font.SysFont("Courier New", 18)
		self.originFont = pygame.font.SysFont("Courier New", 14)
		
		self.lines = []
		self.renderedLines = []

		self.rowOffset = 0
		self.animTimer = 0

		self.numLines = 0
		self.originText = None

		self.generateLines()

	def generateLines(self):
		self.rows = []
		
		numQuotes = 0
		leftOver = ""

		currentQuote = None

		rows = 0
		while (True):
			while (len(leftOver) < MAX_WRITING_COLS):
				if (len(leftOver) > 0):
					self.lines.append(QuoteLine(leftOver, len(self.lines), currentQuote.origin))
				if (numQuotes >= len(self.quoteManager.quotes)):
					leftOver = None
					break
				currentQuote = self.quoteManager.getNearbyQuote(numQuotes)
				leftOver = currentQuote.text
				numQuotes += 1

			if (not leftOver):
				break

			col = MAX_WRITING_COLS - 1
			while (col > 0 and leftOver[col] != " "):
				col -= 1
			if (col <= 0):
				col = MAX_WRITING_COLS - 1

			self.lines.append(QuoteLine(leftOver[:col], len(self.lines), currentQuote.origin))
			leftOver = leftOver[col + 1:]
			rows += 1
		
		self.numLines = len(self.lines)

		# Render the first number of lines
		for i in range(min(MAX_WRITING_ROWS, self.numLines)):
			self.lines[i].renderLine(self.textFont, WHITE)
		self.updateOriginText()

		self.rowOffset = 0

	def updateOriginText(self):
		topLine = self.lines[self.rowOffset]
		self.originText = self.originFont.render(topLine.origin, True, WHITE)

	def moveLines(self):
		oldRowOffset = self.rowOffset
		self.rowOffset += 1
		if (self.rowOffset > self.numLines):
			self.rowOffset = self.numLines
		
		if (self.rowOffset == oldRowOffset):
			return

		if (self.lines[self.rowOffset].origin != self.lines[oldRowOffset].origin):
			self.updateOriginText()
		
		self.lines[oldRowOffset].discardRenderedLine()
		if (self.rowOffset + MAX_WRITING_ROWS <= self.numLines):
			self.lines[self.rowOffset + MAX_WRITING_ROWS - 1].renderLine(self.textFont, WHITE)

	def tick(self):
		self.animTimer += 1
		if (self.animTimer >= 10):
			self.animTimer = 0
			self.moveLines()

	def render(self, screen, dt):
		w = screen.get_width()
		h = screen.get_height()

		y = 100
		alpha = 1.0
		for i in range(min(MAX_WRITING_ROWS, self.numLines - self.rowOffset)):
			line = self.lines[i + self.rowOffset].renderedLine
			
			# Make temp surface for alpha channel
			surface = pygame.Surface((line.get_width(), line.get_height()))
			surface.blit(line,(0, 0))
			
			# Set alpha
			surface.set_alpha(int(alpha * 255))
			alpha -= 1.0 / MAX_WRITING_ROWS
			
			# Draw temp surface to screen
			screen.blit(surface, ((w - line.get_width()) // 2, y))

			y += line.get_height()

		if (self.rowOffset >= 0 and self.rowOffset < self.numLines):
			screen.blit(self.originText, (w - self.originText.get_width() - 5, h - self.originText.get_height() - 5))
