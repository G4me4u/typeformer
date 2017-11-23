from quote import Quote
from random import randint

class QuoteManager:

	def __init__(self, filePath):
		self.filePath = filePath
		self.quotes = []
		
		self.load()

	def load(self):
		for line in open(self.filePath, "r"):
			quote = line.replace("\n", "").split("@")
			if (len(quote) != 2):
				continue
			self.quotes.append(Quote(quote[0], quote[1]))
		
		print(str(self.getRandomQuote()))
	
	def getRandomQuote(self):
		return self.quotes[randint(0, len(self.quotes) - 1)]


