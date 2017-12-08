import pygame

from time import time
from random import shuffle

from constants import *

from quote import Quote
from quoteline import QuoteLine

class QuoteManager:

	def __init__(self, filePath):
		'''
		Initializes QuoteManager. The first argument (filePath) is the
		location of the quote text file. The format used for storing
		these quotes have to be the following:
			[quote-text]@[origin]
		Where quote-text is the actual quote (no new-lines or @ characters)
		and origin is where the text originated from (can be empty).
		'''

		self.filePath = filePath
		self.quotes = []

		# Fonts used for drawing
		self.textFont = pygame.font.SysFont("Courier", 18)
		self.uiFont = pygame.font.SysFont("Courier", 14)

		tmpChar = self.textFont.render(" ", False, BLACK)
		self.charSize = ( tmpChar.get_width(), tmpChar.get_height() )
		
		self.lines = []
		self.renderedLines = []

		self.rowOffset = 0
		self.colOffset = 0

		self.currentText = None
		self.lineTypedText = None
		self.lineMissingText = None
		self.symbolsPerSecondText = None

		self.numLines = 0
		self.originText = None

		self.typedTimes = []
		self.symbolsPerSecond = 0
		
		self.load()

	def load(self):
		'''
		Loads quotes from the given filepath. (see QuoteManager.__init__())
		'''

		for line in open(self.filePath, "r", encoding="utf-8"):
			quote = line.replace("\n", "").split("@")
			if (len(quote) != 2):
				continue
			self.quotes.append(Quote(quote[0], quote[1]))

	def randomize(self):
		'''
		Randomizes the loaded quotes.
		NOTE: if this function is called and lines are already generated,
		they will not be recreated nor discarted. Call generateLines() if
		desired.
		'''

		shuffle(self.quotes)

	def generateLines(self):
		'''
		Generates lines used for drawing and typing. More specifically,
		this funtion will split all the quotes into smaller lines, so
		they fit the specification of MAX_WRITING_COLS in constants.py
		'''

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
		self.symbolsPerSecondText = None

		self.typedTimes = []
		self.symbolsPerSecond = 0

	def updateOriginText(self):
		'''
		Updates the rendered text used to draw the origin of the current
		topLine.
		'''

		origin = self.lines[self.rowOffset].origin
		if (len(origin) > MAX_ORIGIN_LENGTH):
			origin = (origin[:MAX_ORIGIN_LENGTH - 3]) + "..."

		self.originText = self.uiFont.render(origin, False, WHITE)

	def keyTyped(self, key):
		'''
		Should be invoked whenever a key has been pressed. The first
		argument is the unicode char of the KEY_PRESSED event.
		'''

		topLine = self.lines[self.rowOffset]
		if (self.colOffset >= len(topLine.lineText)):
			if (key == " "):
				self.typedTimes.append(time())
				
				self.moveLines()
				self.colOffset = 0
			return
		
		if (key == topLine.lineText[self.colOffset]):
			self.colOffset += 1
			currentlyTyped = topLine.lineText[:self.colOffset]
			
			self.currentText = self.uiFont.render(currentlyTyped, False, WHITE)
			self.lineTypedText = self.textFont.render(currentlyTyped.replace(" ", "_"), False, RED)
			self.lineMissingText = self.textFont.render(topLine.lineText[self.colOffset:], False, WHITE)

			self.typedTimes.append(time())

	def moveLines(self):
		'''
		Increments the rowOffset used for drawing lines onto the screen.
		NOTE: this will not reset colOffset, but it does reinitialize the
		originText (see QuoteManager.updateOriginText()).
		'''

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
		'''
		Ticks this quotemanager. Used for timing the amount of characters typed
		per second.
		'''

		now = time()
		while (len(self.typedTimes) > 0 and now - self.typedTimes[0] > AVG_SPEED_SAMPLE_TIME):
			self.typedTimes.pop(0)
		
		self.symbolsPerSecond = len(self.typedTimes) / AVG_SPEED_SAMPLE_TIME
		self.symbolsPerSecondText = self.uiFont.render(str(self.symbolsPerSecond) + " symbols / s", False, WHITE)

	def renderLine(self, screen, line, x, y, alpha=1.0):
		'''
		Draws a text-line on the specified location with the specified alpha
		'''
		
		# Set alpha
		line.set_alpha(int(alpha * 255))
		screen.blit(line, (x, y))

	def render(self, screen, dt):
		'''
		Draws the currently active text-lines, originText and currently typed text.
		'''

		w = screen.get_width()
		h = screen.get_height()
		
		aw = int(self.charSize[0] * MAX_WRITING_COLS)
		ax = (w - aw) // 2
		y = 20
		ah = self.charSize[1] * MAX_WRITING_ROWS

		tmpSurface = pygame.Surface((aw + 10, ah + 10))
		tmpSurface.set_alpha(128)
		tmpSurface.fill(BLACK)
		screen.blit(tmpSurface, (ax - 5, y - 5))

		if (self.symbolsPerSecondText):
			screen.blit(self.symbolsPerSecondText, ((w - self.symbolsPerSecondText.get_width()) // 2, h - self.charSize[1] * 2 - 10))

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