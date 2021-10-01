# fourtyFive test canvas
#
# Proof of concept MIDI instrument

# using pygame as the canvas https://www.pygame.org/docs/

import math
import pygame # brew install pygame
from pygame.locals import *

class shapeWheel(object):
	def __init__(self, canvasSize, r, sliceNo=1, offsetDegs=0, canvasMargin=10, labelList=[]):
		self.sliceNo = int(sliceNo)
		self.r = int(r)
		self.circleDivisions = 12 # 12-slices around the circle
		self.offsetDegs = int(offsetDegs)
		self.canvasMargin = int(canvasMargin)
		self.originX = int((canvasSize/2) + self.canvasMargin) # Center of the canvas X
		self.originY = int((canvasSize/2) + self.canvasMargin) # Center of the canvas Y
		self.canvasWidth = (canvasSize + (self.canvasMargin * 2))
		self.canvasHeight = (canvasSize + (self.canvasMargin * 2))
		self.labelList = labelList

		self.coords = []

		self.findCoords()

	def findCoords(self):
		for i in range(12):
			self.coords.append( # One corner of the triangle along the circle radius r, at sliceNo*1/12circle degs
				(
					(
						self.originX +
						int(self.r * math.sin(
								math.radians(
									((360/self.circleDivisions) * i) + self.offsetDegs
								)
							)
						)
					),
					(
						self.originY +
						int(self.r * math.cos(
								math.radians(
									((360/self.circleDivisions) * i) + self.offsetDegs
								)
							)
						)
					)
				)
			)

class shapeWheelTriangleSlice(shapeWheel):
	def findCoords(self):
		self.coords.append( # Origin
			(
				self.originX,
				self.originY
			)
		)
		self.coords.append( # One corner of the triangle along the circle radius r, at sliceNo*1/12circle degs
			(
				(
					self.originX +
					int(self.r * math.sin(
							math.radians(
								((360/self.circleDivisions) * self.sliceNo) + self.offsetDegs
							)
						)
					)
				),
				(
					self.originY +
					int(self.r * math.cos(
							math.radians(
								((360/self.circleDivisions) * self.sliceNo) + self.offsetDegs
							)
						)
					)
				)
			)
		)
		self.coords.append(  # One corner of the triangle along the circle radius r, at (sliceNo+1)*1/12circle degs
			(
				(
					self.originX +
					int(self.r * math.sin(
							math.radians(
								((360 / self.circleDivisions) * (self.sliceNo+1)) + self.offsetDegs
							)
						)
					)
				),
				(
					self.originY +
					int(self.r * math.cos(
							math.radians(
								((360 / self.circleDivisions) * (self.sliceNo+1)) + self.offsetDegs
							)
						)
					)
				)
			)
		)

class controlSystem(object):
	def __init__(self, canvasWidth, canvasHeight, canvasMargin, color, bgcolor, notes, blitX, blitY, fontMed):
		self.surface = None
		self.canvasWidth = canvasWidth
		self.canvasHeight = canvasHeight
		self.canvasMargin = canvasMargin
		self.color = color
		self.bgcolor = bgcolor
		self.notes = notes # Holds the dict/lists representing the scale notes, their positions and values, etc
		self.blitX = blitX # The X location in which this entire control should be blit to the screen canvas
		self.blitY = blitY # The Y location in which this entire control should be blit to the screen canvas
		self.fontMed = fontMed # Medium sized font
		self.surface = pygame.Surface((int(self.canvasWidth + (self.canvasMargin * 2)),
									   int(self.canvasHeight + (self.canvasMargin * 2))))

	def initSurface(self):
		pass

	def drawPolygon(self, shape):
		pygame.draw.polygon(self.surface, self.color, shape.coords, 1)

	def drawLabelList(self, shape, labels):
		coordPair = 0
		for coords in shape.coords:
			text = self.fontMed.render(labels[coordPair]['noteName'], False, self.color)
			textXCenter = int(text.get_width() / 2)
			textYCenter = int(text.get_height() / 2)
			# Bit on to the surface:
			self.surface.blit(text, [coords[0] - textXCenter, coords[1] - textYCenter])
			coordPair += 1

	def drawControl(self):
		pass

	def updateControl(self, events):
		pass

class ffWheel(controlSystem):
	def initSurface(self):
		# ffWheel-specific object attributes
		self.r = int(self.canvasHeight/2)
		self.rotateOffset = 0
		self.rotateSteps = 0
		self.rotateIterator = 0
		self.offsetDegs = int(360/24) # Control offset degrees

	def updateControl(self, events):
		for event in events:
			if (event == "K_a"):
				self.rotateSteps = 10
				self.rotateIterator = 1
			if (event == "K_d"):
				self.rotateSteps = 10
				self.rotateIterator = -1
		if self.rotateSteps > 0:
			self.rotateOffset += self.rotateIterator
			self.rotateSteps -= 1

	def drawControl(self):
		self.surface.fill(self.bgcolor)
		# Draw the reference circle
		labelCircle = shapeWheel(canvasSize=self.r*2,
							 r=self.r-50,
							 sliceNo=1,
							 offsetDegs= self.rotateOffset,
							 canvasMargin=self.canvasMargin,
							 labelList=self.notes)
		self.drawLabelList(labelCircle, self.notes)

		# Draw the slices
		for i in range(12):
			polygon = shapeWheelTriangleSlice(canvasSize=self.r*2,
											  r=self.r,
											  sliceNo=i,
											  offsetDegs=self.offsetDegs + self.rotateOffset,
											  canvasMargin=self.canvasMargin)
			self.drawPolygon(polygon)

class fourtyFive:
	def __init__(self, canvasWidth=1920, canvasHeight=1080):

		# Musical attributes
		self.notes = [
			{'noteName': 'c', 'kbNum': 1, 'wheelPos': 1},
			{'noteName': 'g', 'kbNum': 8, 'wheelPos': 2},
			{'noteName': 'd', 'kbNum': 3, 'wheelPos': 3},
			{'noteName': 'a', 'kbNum': 10, 'wheelPos': 4},
			{'noteName': 'e', 'kbNum': 5, 'wheelPos': 5},
			{'noteName': 'b', 'kbNum': 12, 'wheelPos': 6},
			{'noteName': 'gb/f#', 'kbNum': 7, 'wheelPos': 7},
			{'noteName': 'db/c#', 'kbNum': 2, 'wheelPos': 8},
			{'noteName': 'ab/g#', 'kbNum': 9, 'wheelPos': 9},
			{'noteName': 'eb/d#', 'kbNum': 4, 'wheelPos': 10},
			{'noteName': 'bb/a#', 'kbNum': 11, 'wheelPos': 11},
			{'noteName': 'f', 'kbNum': 6, 'wheelPos': 12}
		]

		# Graphics attributes

		self.canvasWidth = canvasWidth
		self.canvasHeight = canvasHeight

		self.r = int((canvasHeight * .8)/2) # R is half of __% of the screen
		self.canvasMargin = 10

		# Define some colors for convenience and readability
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.red = (255,0,0)
		self.orange = (255,94,19)

		self.running = False # will be True once self.run() is called

		# Initialize the canvas
		pygame.init()
		self.canvas = pygame.display.set_mode([self.canvasWidth, self.canvasHeight])
		pygame.display.set_caption('fourtyFive')  # Set the window title for fun

		self.centerX = self.canvas.get_rect().centerx
		self.centerY = self.canvas.get_rect().centery
		self.bottom  = self.canvas.get_rect().bottom

		# fonts = pygame.font.get_fonts()
		# print(len(fonts))
		# for f in fonts:
		# 	print(f)

		# Initialize a font.  This takes forever, like maybe 8 seconds.  But happens once.
		self.fontMed = pygame.font.SysFont('courier', 32)

		# controlSurfaces list contains each controlSystem object that is rendered.
		# Declare controlSystem objects, set them up and init them, then append() them
		# to this list.  Then each in turn will get a drawControl() call and their
		# surface attribute will be blit to the cancas.
		self.controlSurfaces = []

		# The size of the ffWheel's surface will be __% of the screen
		controlFfWheelSize = int(self.canvasHeight * 0.8)
		# Create a ffWheel control.  Init.
		controlFfWheel = ffWheel(controlFfWheelSize, controlFfWheelSize,  # Size of this control's surface.
								 self.canvasMargin, # render margin
								 self.orange, self.black, # fgcolor and bgcolor
								 self.notes,  # list of note vals
								 int((self.canvasWidth / 2) - (controlFfWheelSize/2)), 0, # Blit loc on the screen
								 self.fontMed)
		controlFfWheel.initSurface()
		# Rotate 360?
		# controlFfWheel.rotateSteps = 360
		# controlFfWheel.rotateIterator = -1
		# Append the ffWheel to the controlSurfaces list
		self.controlSurfaces.append(controlFfWheel)

	def run(self):
		self.running = True

		self.canvas.fill(self.black)  # fill the screen with black

		# The main running loop
		while self.running:

			# First, draw the screen:
			# Loop through each controlSystem added to the controlSurfaces list
			for controlSurface in self.controlSurfaces:
				# The drawControl method should update the control's visual elements and
				# draw to the control's surface
				controlSurface.drawControl()
				# Blit the control's surface to the canvas
				self.canvas.blit(controlSurface.surface, [controlSurface.blitX, controlSurface.blitY])
			pygame.display.update()

			# Next, Update controls and everything in preparation for the next loop through:
			events = {} # Record events seen during this execution here.  Key is a label, usually pygame event
			# The controlSurfaces themselves should know what to look for and what to do.
			for event in pygame.event.get():
				if event.type == QUIT:  # If the window 'close' button is clicked...
					self.running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_a:
						events["K_a"]=True
					if event.key == pygame.K_d:
						events["K_d"]=True
			for controlSurface in self.controlSurfaces:
				controlSurface.updateControl(events) # update control attributes based on what needs to happen

		# If we've reached this point, we've escaped the run: loop.  Quittin' time.
		pygame.quit()

def test_fourtyFive_healthCheck_topLevel():
	# pytest assertion
	fourtyFiveTestObj = None
	fourtyFiveTestObj = fourtyFive()
	# Top level healthcheck - everything initialized and there is at least 1 control surface
	assert len(fourtyFiveTestObj.controlSurfaces) > 0

if __name__ == "__main__":
	fourtyFive = fourtyFive()
	fourtyFive.run()