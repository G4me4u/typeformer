
class QuoteLine:

	def __init__(self, lineText, lineNumber, origin):
		self.lineText = lineText
		self.lineNumber = lineNumber
		self.origin = origin

		self.renderedLine = None

	def renderLine(self, font, color):
		self.renderedLine = font.render(self.lineText, True, color)

	def discardRenderedLine(self):
		self.renderedLine = None