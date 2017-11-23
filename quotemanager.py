from quote import Quote
from random import shuffle

class QuoteManager:

	def __init__(self, filePath):
		self.filePath = filePath
		self.quotes = []

		self.currentQuoteIndex = 0
		self.currentQuoteOffset = 0
		
		self.load()

	def load(self):
		for line in open(self.filePath, "r"):
			quote = line.replace("\n", "").split("@")
			if (len(quote) != 2):
				continue
			self.quotes.append(Quote(quote[0], quote[1]))
	
	def randomize(self):
		shuffle(self.quotes)

	def getCurrentQuote(self):
		return self.getNearbyQuote(0)

	def getNearbyQuote(self, currentIndexOffset):
		return self.quotes[self.currentQuoteIndex + currentIndexOffset]

