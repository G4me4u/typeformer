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

'''
Initializes the timer. Has to be invoked before running
main loop. This function will set up time constants
aswell as the tpsGoal provided as an argument.
'''
	def initTimer(self, tpsGoal):
		self.tpsGoal = tpsGoal

		self.last = time()
		self.dt = 1.0
		self.ds = 0.0
		self.missingTicks = 0

'''
Ticks this timer. Has to be invoked everytime one
wants to know if there are any missingTicks to be
handled. This function will calculate the delta time
and use it for calculating the missingTicks variable.
'''
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

'''
Should be invoked whenever a tick has passed (used for debugging)
'''
	def tickPassed(self):
		self.tps += 1

'''
Should be invoked whenever a frame has passed (used for debugging)
'''
	def framePassed(self):
		self.fps += 1