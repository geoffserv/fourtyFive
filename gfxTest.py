# fourtyFive test canvas
#
# Proof of concept MIDI instrument

# using pygame as the canvas https://www.pygame.org/docs/

import pygame # brew install pygame
from pygame.locals import *

class screen:
	def __init__(self, canvasWidth=1028, canvasHeight=720):
		pygame.init()
		self.canvas = pygame.display.set_mode([1280,720]) # 16x9 SD for later capture in to VDMX
		pygame.display.set_caption('fourtyFive') # Set the window title for fun

		self.centerX = self.canvas.get_rect().centerx
		self.centerY = self.canvas.get_rect().centery
		self.bottom  = self.canvas.get_rect().bottom

		print("DEBUG -- screen_centerX:", self.centerX)
		print("DEBUG -- screen_centerY:", self.centerY)
		print("DEBUG -- screen_bottom:", self.bottom)

		# Define some colors for convenience and readability
		self.black = (0,0,0)
		self.white = (255,255,255)
		self.red = (255,0,0)

		self.running = True # Start off in a running state.  When untrue, the program ends.

# fontObject = pygame.font.SysFont('Courier', 5).render(listLines.pop(0), True, red)

if __name__ == "__main__":
	fourtyFive = screen()
	while fourtyFive.running:
			fourtyFive.canvas.fill(fourtyFive.black) # fill the screen with black, obliterating everything

			# screen.blit(listCrawlers[0][0], render_position)

			pygame.display.update()

			for event in pygame.event.get():
				if event.type == QUIT: # If the window 'close' button is clicked...
					fourtyFive.running = False

	pygame.quit()
