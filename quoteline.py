
class QuoteLine:

	def __init__(self, lineText, lineNumber, origin):
		self.lineText = lineText
		self.lineNumber = lineNumber
		self.origin = origin

		self.renderedLine = None

'''
Renders the line using the given font and color.
'''
	def renderLine(self, font, color):
		self.renderedLine = font.render(self.lineText, True, color)

'''
Discards the rendered line (self.renderedLine = None)
'''
	def discardRenderedLine(self):
		self.renderedLine = None