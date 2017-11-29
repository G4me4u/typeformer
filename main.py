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

'''
Entry-point for program. Here we initialize,
run and stop the execution.
'''
	def start(self):
		self.init()
		self.runLoop()
		self.stop()

'''
Initializes Main
'''
	def init(self):
		self.timer = Timer()

		self.initPygame()
		
		self.quoteManager = QuoteManager(QUOTES_FILE_PATH)
		self.quoteManager.randomize()
		self.quoteManager.generateLines()
	
'''
Initializes pygame and opens a display for drawing.
'''
	def initPygame(self):
		pygame.init()

		pygame.display.set_caption(TITLE)

		size = width, height = 720, 540
		self.screen = pygame.display.set_mode(size)

'''
Handles events sent by pygame (given in arg 1)
'''
	def handleEvent(self, ev):
		if (ev.type == pygame.QUIT):
			self.running = False
		elif (ev.type == pygame.KEYDOWN):
			self.quoteManager.keyTyped(ev.unicode)

'''
Runs the main loop, ticks and draws depending on the
settings of the pre-initialized timer object.
'''
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

'''
Deinitializes pygame and teminates runtime.
'''
	def stop(self):
		pygame.quit()
		exit(0)

'''
Handles ticking of things that need to change.
Called a set amount of time every second (see constants.py)
'''
	def tick(self):
		self.px = self.x
		self.x += 10

		self.quoteManager.tick()

'''
Handles drawing things to the screen.
Called with no specific time interval.
'''
	def draw(self, dt):
		self.screen.fill(BLACK)
		self.render(dt)
		pygame.display.flip()
	
	def render(self, dt):
		self.quoteManager.render(self.screen, dt)

# Start main program
Main().start()