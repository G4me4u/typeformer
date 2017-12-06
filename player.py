from constants import *
from spritesheet import SpriteSheet
from animation import Animation

class Player:

	def __init__(self, quoteManager):
		self.quoteManager = quoteManager

		self.idleAnim = Animation(SpriteSheet(PLAYER_IDLE_PATH, 19, 26), 4, 0.5)
		self.walkAnim = Animation(SpriteSheet(PLAYER_WALK_PATH, 19, 26), 9, 0.25)
		self.runAnim = Animation(SpriteSheet(PLAYER_RUN_PATH, 19, 26), 5, 0.1)

		self.anims = [ self.idleAnim, self.walkAnim, self.runAnim ]
		self.currentAnim = 0

		# Get the width and height from the SpriteSheet
		self.width  = self.idleAnim.sheet.tw
		self.height = self.idleAnim.sheet.th

		self.prevPos = 0
		self.pos = 0

	def reset(self):
		self.pos = 0
		self.prevPos = 0
		self.currentAnim = 0

	def tick(self):
		speed = self.quoteManager.symbolsPerSecond / 3.0

		self.prevPos = self.pos
		self.pos += max(0.0, speed - 1.0) * PLAYER_SPEED

		self.currentAnim = min(2, int(speed))

		self.idleAnim.timePerFrame = max(0.75 * (1.0 - speed), 0.2  )
		self.walkAnim.timePerFrame = max(0.25 * (2.0 - speed), 0.1  )
		self.runAnim.timePerFrame  = max(0.10 * (3.0 - speed), 0.025)

		self.idleAnim.tick()
		self.walkAnim.tick()
		self.runAnim.tick()

	def render(self, screen, dt, offset):
		w = screen.get_width()
		h = screen.get_height()

		pos = self.prevPos + (self.pos - self.prevPos) * dt
		xp = (w - self.width) // 2 + pos - offset
		yp = h - self.height - FLOOR_HEIGHT

		self.anims[self.currentAnim].render(screen, xp, yp)
	