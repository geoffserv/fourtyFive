# fourtyFive test canvas
#
# Proof of concept MIDI instrument

# using pygame as the canvas https://www.pygame.org/docs/

import math
import pygame # brew install pygame
from pygame.locals import *

class triangleSlice:
	def __init__(self, r, sliceNo=0):
		self.sliceNo = sliceNo
		self.r = r
		triangleCoords = []
		triangleCoords.append( # Origin
			(
				(self.wheelr +
				 self.canvasMargin),
				(self.wheelr +
				 self.canvasMargin)
			)
		)
		triangleCoords.append( #
			(
				(
					self.wheelr +
					self.canvasMargin +
					int(1 * self.wheelr * math.sin(
							math.radians(
								(self.twelvthOfCircleDegs * i) + self.twentyFourthOfCircleDegs
							)
						)
					)
				),
				(
					self.wheelr +
					self.canvasMargin +
					int(1 * self.wheelr * math.cos(
							math.radians(
								(self.twelvthOfCircleDegs * i) + self.twentyFourthOfCircleDegs
							)
						)
					)
				)
			)
		)
		print(guideCircle)
		renderposition = [0, 0]

		polygon = pygame.Surface((self.wheelCanvas, self.wheelCanvas))
		pygame.draw.polygon(polygon, self.orange, guideCircle, 1)



class fourtyFive:
	def __init__(self, canvasWidth=1028, canvasHeight=720):
		pygame.init()
		self.canvas = pygame.display.set_mode([canvasWidth,canvasHeight]) # 16x9 SD for later capture in to VDMX
		pygame.display.set_caption('fourtyFive') # Set the window title for fun

		self.width = canvasWidth
		self.height = canvasHeight
		self.centerX = self.canvas.get_rect().centerx
		self.centerY = self.canvas.get_rect().centery
		self.bottom  = self.canvas.get_rect().bottom

		self.twelvthOfCircleDegs = int(360 / 12)
		self.twentyFourthOfCircleDegs = int(360 / 24)

		self.wheelr = int((canvasHeight * .8)/2) # R is half of __% of the screen
		self.canvasMargin = 10
		self.wheelCanvas = int((self.wheelr * 2) + (self.canvasMargin * 2)) # Add the margin all around

		print("DEBUG -- screen_width:", self.width)
		print("DEBUG -- screen_height:", self.height)
		print("DEBUG -- screen_bottom:", self.bottom)
		print("DEBUG -- screen_centerX:", self.centerX)
		print("DEBUG -- screen_centerY:", self.centerY)
		print("DEBUG -- screen_bottom:", self.bottom)

		# Define some colors for convenience and readability
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.red = (255,0,0)
		self.orange = (255,94,19)

		self.running = False # will be True once self.run() is called

		self.run()

	def run(self):
		self.running = True
		guideCircle = []
		for i in range(12):
			guideCircle.append(
				(self.wheelr +
				 self.canvasMargin +
				 int(1 * self.wheelr * math.sin(
					                   		math.radians(
												(self.twelvthOfCircleDegs * i) + self.twentyFourthOfCircleDegs
											)
				 						)
					 ),
				 self.wheelr +
				 self.canvasMargin +
				 int(1 * self.wheelr * math.cos(
											 math.radians(
												 (self.twelvthOfCircleDegs * i) + self.twentyFourthOfCircleDegs
											 )
										 )
					 )
				 )
		 	)
		print(guideCircle)
		renderposition = [0, 0]

		polygon = pygame.Surface((self.wheelCanvas, self.wheelCanvas))
		pygame.draw.polygon(polygon, self.orange, guideCircle, 1)

		while self.running:
			self.canvas.fill(self.black)  # fill the screen with black, obliterating everything

			self.canvas.blit(polygon, renderposition)

			pygame.display.update()

			for event in pygame.event.get():
				if event.type == QUIT:  # If the window 'close' button is clicked...
					self.running = False

		pygame.quit()

# fontObject = pygame.font.SysFont('Courier', 5).render(listLines.pop(0), True, red)

if __name__ == "__main__":
	fourtyFive = fourtyFive()