import pygame

from constants import *
from timer import Timer

from quotemanager import QuoteManager

class Main:

	def __init__(self):
		self.timer = None
		self.screen = None

		self.quoteManager = None

		self.running = False

		self.x = 0
		self.px = self.x

	def start(self):
		self.init()
		self.runLoop()
		self.stop()

	def init(self):
		self.timer = Timer()

		self.initPygame()
		
		self.quoteManager = QuoteManager(QUOTES_FILE_PATH)
		self.quoteManager.randomize()
	
	def initPygame(self):
		pygame.init()

		pygame.display.set_caption(TITLE)

		size = width, height = 720, 540
		self.screen = pygame.display.set_mode(size)

	def handleEvent(self, ev):
		if (ev.type == pygame.QUIT):
			self.running = False
		if (ev.type == pygame.KEYDOWN):
			self.keyTyped(ev.unicode)

	def keyTyped(self, key):
		if key == 'A': #getNextChar():
			pass #addAcceleration()
		else:
			pass #check for jump, or decelerate

	def runLoop(self):
		self.running = True

		self.timer.initTimer(TPS)

		while (self.running):
			for ev in pygame.event.get():
				self.handleEvent(ev)

			self.timer.tick()

			for i in range(self.timer.missingTicks):
				self.tick()
				self.timer.tickPassed()
			
			self.draw(self.timer.dt)
			self.timer.framePassed()

	def stop(self):
		pygame.quit()
		exit(0)

	def tick(self):
		self.px = self.x
		self.x += 10

		self.quoteManager.tick()

	def draw(self, dt):
		self.screen.fill(BLACK)
		self.render(dt)
		pygame.display.flip()
	
	def render(self, dt):
		self.quoteManager.render(self.screen, dt)

Main().start()