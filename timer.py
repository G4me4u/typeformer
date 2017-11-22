from time import time

class Timer:

	def __init__(self):
		self.tps = 0.0

		self.last = 0
		self.dt = 0.0
		self.ds = 0.0
		self.missingTicks = 0

		self.tps = 0
		self.fps = 0
	
# Runtime functions

	def initTimer(self, tpsGoal):
		self.tpsGoal = tpsGoal

		self.last = time()
		self.dt = 1.0
		self.ds = 0.0
		self.missingTicks = 0

	def tick(self):
		now = time()
		deltaS = now - self.last
		self.last = now

		self.ds += deltaS

		self.dt += deltaS * self.tpsGoal
		self.missingTicks = int(self.dt)
		self.dt -= self.missingTicks

		if (self.ds >= 1.0):
			print("tps: " + str(self.tps), "fps: " + str(self.fps))
			self.ds = 0.0
			self.tps = 0
			self.fps = 0

# Debug specific functions

	def tickPassed(self):
		self.tps += 1

	def framePassed(self):
		self.fps += 1