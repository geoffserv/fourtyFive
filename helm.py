# helm
#
# Proof of concept MIDI instrument

# using pygame as the canvas https://www.pygame.org/docs/

import pygame
from pygame.locals import *
from helm_controls import WheelControl

# Griffin Powermate support for Linux systems only
# Can't even install the downstream dependency evdev unless running linux,
# part of the install process checks for kernel header files and so on.
# If in linux, set to True and connect two Powermates for knob support
# Make sure to add the current, non-root UNIX user to the input group
# in /etc/group, and then re-login.  Otherwise, permission errors
using_griffin_powermate = False
if using_griffin_powermate:
    from pypowermate import Powermate

class Helm:
    def __init__(self, canvas_width=1920, canvas_height=1080, init_gfx=True):

        self.powermate = None
        if using_griffin_powermate:
            self.powermate = Powermate('/dev/input/by-id/usb-Griffin_Technology__Inc._Griffin_PowerMate-event-if00')

        # Musical attributes
        self.notes = [
            {'noteName': 'C', 'kbNum': 1, 'wheelPos': 1},
            {'noteName': 'G', 'kbNum': 8, 'wheelPos': 2},
            {'noteName': 'D', 'kbNum': 3, 'wheelPos': 3},
            {'noteName': 'A', 'kbNum': 10, 'wheelPos': 4},
            {'noteName': 'E', 'kbNum': 5, 'wheelPos': 5},
            {'noteName': 'B', 'kbNum': 12, 'wheelPos': 6},
            {'noteName': 'Gb/F#', 'kbNum': 7, 'wheelPos': 7},
            {'noteName': 'Db/C#', 'kbNum': 2, 'wheelPos': 8},
            {'noteName': 'Ab/G#', 'kbNum': 9, 'wheelPos': 9},
            {'noteName': 'Eb/D#', 'kbNum': 4, 'wheelPos': 10},
            {'noteName': 'Bb/A#', 'kbNum': 11, 'wheelPos': 11},
            {'noteName': 'F', 'kbNum': 6, 'wheelPos': 12}
        ]

        # Graphics attributes
        # Clock, for tracking events and frame rate
        self.clock = pygame.time.Clock()

        self.fullscreen = False

        self.canvas_width = canvas_width
        self.canvas_height = canvas_height

        self.r = int(
            (canvas_height * .8) / 2)  # R is half of __% of the screen
        self.canvas_margin = 10

        # Define some colors for convenience and readability
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.orange = (255, 94, 19)
        self.orange_25 = (64, 23, 4)
        self.orange_50 = (128, 47, 9)
        self.orange_75 = (191, 69, 13)

        self.running = False  # will be True once self.run() is called

        # Initialize the canvas
        pygame.init()

        if init_gfx:
            # If this is being run headless, turn initGfx to False
            # This is useful for headless CI testing
            if self.fullscreen:
                self.canvas = pygame.display.set_mode(
                    (0,0), pygame.FULLSCREEN)
            else:
                self.canvas = pygame.display.set_mode(
                    [self.canvas_width, self.canvas_height])
            pygame.display.set_caption('helm')  # Set the window title for fun

        # Fonts - very slow
        # Initialize a font.  This takes forever, like maybe 8 seconds.  But
        # happens once.
        self.font_small = pygame.font.SysFont('courier', 24)
        self.font_med = pygame.font.SysFont('courier', 32)
        self.font_x_large = pygame.font.SysFont('courier', 80)
        # Listing available fonts, fun for later:
        # fonts = pygame.font.get_fonts()
        # print(len(fonts))
        # for f in fonts:
        # 	print(f)

        # controlSurfaces list contains each controlSystem object that is
        # rendered.
        # Declare controlSystem objects, set them up and init them,
        # then append() them
        # to this list.  Then each in turn will get a drawControl() call and
        # their
        # surface attribute will be blit to the canvas.
        self.controlSurfaces = []

        # The size of the ffWheel's surface will be __% of the screen
        control_ff_wheel_size = int(self.canvas_height * 0.98)
        # Create a ffWheel control.  Init.
        control_ff_wheel = WheelControl(control_ff_wheel_size,
                                        control_ff_wheel_size,
                                        # Size of this control's surface.
                                        self.canvas_margin,  # render margin
                                        self.orange, self.black,
                                        # fg color and bg color
                                        self.orange_25,  # accent color
                                        self.notes,  # list of note values
                                        self.canvas_margin,
                                        self.canvas_margin,  # Blit location
                                        self.font_small,
                                        self.font_med,
                                        self.font_x_large)

        # Append the ffWheel to the controlSurfaces list
        self.controlSurfaces.append(control_ff_wheel)

    def run(self):
        self.running = True

        self.canvas.fill(self.black)  # fill the screen with black

        # The main running loop
        while self.running:

            # First, draw the screen:
            # Loop through each controlSystem added to the controlSurfaces list
            for controlSurface in self.controlSurfaces:
                # The drawControl method should update the control's visual
                # elements and
                # draw to the control's surface
                controlSurface.draw_control()
                # Blit the control's surface to the canvas
                self.canvas.blit(controlSurface.surface,
                                 [controlSurface.blit_x,
                                  controlSurface.blit_y])
            pygame.display.update()

            # Next, Update controls and everything in preparation for the
            # next loop through:
            events = {}  # Record events seen during this execution here.
            # Key is a label, usually pygame event
            # The controlSurfaces themselves should know what to look for
            # and what to do.
            for event in pygame.event.get():
                if event.type == QUIT:  # If the window 'close' button...
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_a:
                        events["K_a"] = True
                    if event.key == pygame.K_d:
                        events["K_d"] = True
                    if event.key == pygame.K_q:
                        events["K_q"] = True
                    if event.key == pygame.K_e:
                        events["K_e"] = True

            if using_griffin_powermate:
                event = self.powermate.read_event(timeout=0)
                if event:
                    if event[2] == 1:
                        events["K_a"] = True
                    if event[2] == -1:
                        events["K_d"] = True

            for controlSurface in self.controlSurfaces:
                controlSurface.update_control(
                    events)  # update control attributes with a dict of events

            self.clock.tick(60)  # 60 fps

        # If we've reached this point, we've escaped the run: loop.  Quit.
        pygame.quit()


if __name__ == "__main__":
    helm = Helm()
    helm.run()
