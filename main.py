import pygame

from constants import *
from timer import Timer

class Main:

	def __init__(self):
		self.timer = None
		self.screen = None

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
	
	def initPygame(self):
		pygame.init()

		size = width, height = 1200, 800
		self.screen = pygame.display.set_mode(size)

	def runLoop(self):
		self.running = True

		self.timer.initTimer(TPS)

		while (self.running):
			for ev in pygame.event.get():
				if (ev.type == pygame.QUIT):
					self.running = False

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

	def draw(self, dt):
		self.screen.fill(black)
		self.render(dt)
		pygame.display.flip()
	
	def render(self, dt):
		pygame.draw.rect(self.screen, (255, 255, 255), pygame.Rect(self.px + (self.x - self.px) * dt, 10, 100, 100))

Main().start()