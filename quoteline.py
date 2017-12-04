
class QuoteLine:

	def __init__(self, lineText, lineNumber, origin):
		self.lineText = lineText
		self.lineNumber = lineNumber
		self.origin = origin

		self.renderedLine = None

	def renderLine(self, font, color):
		'''
		Renders the line using the given font and color.
		'''

		self.renderedLine = font.render(self.lineText, False, color)

	def discardRenderedLine(self):
		'''
		Discards the rendered line (self.renderedLine = None)
		'''
		
		self.renderedLine = None