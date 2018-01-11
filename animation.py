from time import time

class Animation:

	def __init__(self, sheet, cols, timePerFrame):
		self.sheet = sheet
		self.cols = cols
		self.timePerFrame = timePerFrame

		self.last = time()
		self.animProgress = 0.0

		self.col = 0

	def tick(self):
		'''
		Updates the current animation frame
		depending on the time passed.
		'''

		now = time()
		self.animProgress += (now - self.last) / self.timePerFrame
		self.last = now

		while (self.animProgress >= 1.0):
			self.animProgress -= 1.0
			self.col += 1
			if (self.col >= self.cols):
				self.col = 0

	def render(self, screen, x, y):
		'''
		Draws the current animation frame
		'''
		
		self.sheet.render(screen, x, y, self.col, 0)