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

	def start(self):
		'''
		Entry-point for program. Here we initialize,
		run and stop the execution.
		'''
		
		self.init()
		self.runLoop()
		self.stop()

	def init(self):
		'''
		Initializes Main
		'''
		
		self.timer = Timer()

		self.initPygame()
		
		self.quoteManager = QuoteManager(QUOTES_FILE_PATH)
		self.quoteManager.randomize()
		self.quoteManager.generateLines()
	
	def initPygame(self):
		'''
		Initializes pygame and opens a display for drawing.
		'''
		
		pygame.init()

		pygame.display.set_caption(TITLE)

		size = width, height = 720, 540
		self.screen = pygame.display.set_mode(size)

	def handleEvent(self, ev):
		'''
		Handles events sent by pygame (given in arg 1)
		'''

		if (ev.type == pygame.QUIT):
			self.running = False
		elif (ev.type == pygame.KEYDOWN):
			self.quoteManager.keyTyped(ev.unicode)

	def runLoop(self):
		'''
		Runs the main loop, ticks and draws depending on the
		settings of the pre-initialized timer object.
		'''

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
		'''
		Deinitializes pygame and teminates runtime.
		'''

		pygame.quit()
		exit(0)

	def tick(self):
		'''
		Handles ticking of things that need to change.
		Called at a set time interval (see constants.py)
		'''

		self.quoteManager.tick()

	def draw(self, dt):
		'''
		Handles drawing things to the screen.
		Called with no specific time interval.
		'''

		self.screen.fill(BLACK)
		self.render(dt)
		pygame.display.flip()
	
	def render(self, dt):
		self.quoteManager.render(self.screen, dt)

# Start main program
Main().start()