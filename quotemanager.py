import pygame

from time import time
from random import shuffle

from constants import *

from quote import Quote
from quoteline import QuoteLine

class QuoteManager:

	def __init__(self, filePath):
		self.filePath = filePath
		self.quotes = []

		self.textFont = pygame.font.SysFont("Courier New", 18)
		self.originFont = pygame.font.SysFont("Courier New", 14)
		
		self.lines = []
		self.renderedLines = []

		self.rowOffset = 0
		self.colOffset = 0
		self.animTimer = 0

		self.currentText = None
		self.lineTypedText = None
		self.lineMissingText = None

		self.numLines = 0
		self.originText = None

		self.typedTimes = []
		self.symbolsPerSecond = 0
		
		self.load()

	def load(self):
		for line in open(self.filePath, "r"):
			quote = line.replace("\n", "").split("@")
			if (len(quote) != 2):
				continue
			self.quotes.append(Quote(quote[0], quote[1]))
	
	def randomize(self):
		shuffle(self.quotes)

	def generateLines(self):
		self.lines = []
		
		numQuotes = 0
		leftOver = ""

		currentQuote = None

		rows = 0
		while (True):
			while (len(leftOver) < MAX_WRITING_COLS):
				if (len(leftOver) > 0):
					self.lines.append(QuoteLine(leftOver, len(self.lines), currentQuote.origin))
				if (numQuotes >= len(self.quotes)):
					leftOver = None
					break
				currentQuote = self.quotes[numQuotes]
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
		self.colOffset = 0
		self.currentText = None
		self.lineTypedText = None
		self.lineMissingText = None

		self.typedTimes = []
		self.symbolsPerSecond = 0

	def updateOriginText(self):
		topLine = self.lines[self.rowOffset]
		self.originText = self.originFont.render(topLine.origin, True, WHITE)

	def keyTyped(self, key):
		topLine = self.lines[self.rowOffset]
		if (self.colOffset >= len(topLine.lineText)):
			if (key == " "):
				self.moveLines()
				self.colOffset = 0
			return
		
		if (key == topLine.lineText[self.colOffset]):
			self.colOffset += 1
			currentlyTyped = topLine.lineText[:self.colOffset]
			
			self.currentText = self.originFont.render(currentlyTyped, True, WHITE)
			self.lineTypedText = self.textFont.render(currentlyTyped.replace(" ", "_"), True, RED)
			self.lineMissingText = self.textFont.render(topLine.lineText[self.colOffset:], True, WHITE)

			self.typedTimes.append(time())

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
		now = time()
		while (len(self.typedTimes) > 0 and now - self.typedTimes[0] > AVG_SPEED_SAMPLE_TIME):
			self.typedTimes.pop(0)
		
		self.symbolsPerSecond = len(self.typedTimes) / AVG_SPEED_SAMPLE_TIME

	def renderLine(self, screen, line, x, y, alpha=1.0):
		# Make temp surface for alpha channel
		surface = pygame.Surface((line.get_width(), line.get_height()))
		surface.blit(line,(0, 0))
		
		# Set alpha
		surface.set_alpha(int(alpha * 255))
		
		# Draw temp surface to screen
		screen.blit(surface, (x, y))

	def render(self, screen, dt):
		w = screen.get_width()
		h = screen.get_height()

		y = 20
		alpha = 1.0
		for i in range(min(MAX_WRITING_ROWS, self.numLines - self.rowOffset)):
			line = self.lines[i + self.rowOffset]
			if (i == 0 and self.colOffset > 0):
				x0 = (w - self.lineTypedText.get_width() - self.lineMissingText.get_width()) // 2
				x1 = x0 + self.lineTypedText.get_width()

				self.renderLine(screen, self.lineTypedText, x0, y)
				self.renderLine(screen, self.lineMissingText, x1, y)
			else:
				self.renderLine(screen, line.renderedLine, (w - line.renderedLine.get_width()) // 2, y, alpha)
			
			alpha -= 1.0 / MAX_WRITING_ROWS
			y += line.renderedLine.get_height()

		if (self.rowOffset >= 0 and self.rowOffset < self.numLines):
			screen.blit(self.originText, (w - self.originText.get_width() - 5, h - self.originText.get_height() - 5))

		if (self.currentText):
			screen.blit(self.currentText, (5, h - self.currentText.get_height() - 5))