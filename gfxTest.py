# helm test canvas
#
# Proof of concept MIDI instrument

# using pygame as the canvas https://www.pygame.org/docs/

import math
import pygame
from pygame.locals import *


class ShapeWheel(object):
    def __init__(self, canvas_size, r, slice_no=1, offset_degrees=0,
                 canvas_margin=10, label_list=None):
        self.slice_no = int(slice_no)
        self.r = int(r)
        self.circle_divisions = 12  # 12-slices around the circle
        self.offset_degrees = int(offset_degrees)
        self.canvas_margin = int(canvas_margin)
        self.origin_x = int(
            (canvas_size / 2) + self.canvas_margin)  # Center of the canvas X
        self.origin_y = int(
            (canvas_size / 2) + self.canvas_margin)  # Center of the canvas Y
        self.canvas_width = (canvas_size + (self.canvas_margin * 2))
        self.canvas_height = (canvas_size + (self.canvas_margin * 2))
        self.label_list = label_list

        # offset_orientation is a number of degrees added to everything
        # to set an overall coordinate system orientation
        self.offset_orientation = 90

        # list of coordinates representing this shape
        self.coordinates = []
        # associates list of degrees from the origin for each coordinate pair
        self.degrees = []
        self.find_coordinates()

    def find_coordinates(self):
        for i in range(12):
            self.coordinates.append(
                # One corner of the triangle along the circle radius r,
                # at sliceNo*1/12circle
                (
                    (
                        self.origin_x -
                        int(self.r * math.cos(
                            math.radians(
                                ((360 / self.circle_divisions) * i)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    ),
                    (
                        self.origin_y -
                        int(self.r * math.sin(
                            math.radians(
                                ((360 / self.circle_divisions) * i)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    )
                )
            )
            self.degrees.append(
                int(-((360 / self.circle_divisions) * i))
                - self.offset_degrees
            )


class ShapeWheelSlice(ShapeWheel):
    def find_coordinates(self):
        self.coordinates.append(  # Origin
            (
                self.origin_x,
                self.origin_y
            )
        )
        self.coordinates.append(
            # One corner of the triangle along the circle radius r,
            # at sliceNo*1/12circle
            (
                (
                    self.origin_x -
                    int(self.r * math.cos(
                        math.radians(
                            ((360 / self.circle_divisions) *
                             self.slice_no) + self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                ),
                (
                    self.origin_y -
                    int(self.r * math.sin(
                        math.radians(
                            ((360 / self.circle_divisions) *
                             self.slice_no) + self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                )
            )
        )
        self.coordinates.append(
            # One corner of the triangle along the circle radius r,
            # at (sliceNo+1)*1/12circle
            (
                (
                    self.origin_x -
                    int(self.r * math.cos(
                        math.radians(
                            ((360 / self.circle_divisions) * (
                                        self.slice_no + 1)) +
                            self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                ),
                (
                    self.origin_y -
                    int(self.r * math.sin(
                        math.radians(
                            ((360 / self.circle_divisions) * (
                                        self.slice_no + 1)) +
                            self.offset_degrees
                            + self.offset_orientation
                            ))
                        )
                )
            )
        )
        self.degrees.append(
            int(-((360 / self.circle_divisions) * self.slice_no))
            - self.offset_degrees
        )


class ShapeWheelRay(ShapeWheel):
    def find_coordinates(self):
        self.coordinates.append(  # Origin
            (
                self.origin_x,
                self.origin_y
            )
        )
        self.coordinates.append(
                (
                    (
                        self.origin_x -
                        int(self.r * math.cos(
                            math.radians(
                                ((360 / self.circle_divisions) * self.slice_no)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    ),
                    (
                        self.origin_y -
                        int(self.r * math.sin(
                            math.radians(
                                ((360 / self.circle_divisions) * self.slice_no)
                                + self.offset_degrees
                                + self.offset_orientation
                                ))
                            )
                    )
                )
            )
        self.degrees.append(
            int(-((360 / self.circle_divisions) * self.slice_no))
            - self.offset_degrees
        )


class ControlSystem(object):
    def __init__(self, canvas_width, canvas_height, canvas_margin, color,
                 color_bg, color_accent, notes, blit_x, blit_y, font_small,
                 font_medium, font_x_large):
        self.surface = None
        self.canvas_width = canvas_width
        self.canvas_height = canvas_height
        self.canvas_margin = canvas_margin
        self.color = color
        self.color_bg = color_bg
        self.color_accent = color_accent
        self.notes = notes  # Holds the dict/lists representing the scale
        # notes, their positions and values, etc
        self.key = 0  # Key is the index of the notes dict indicating the key
        self.note_selection = 0  # The currently selected note index
        self.blit_x = blit_x  # The X location in which this entire control
        # should be blit to the screen canvas
        self.blit_y = blit_y  # The Y location in which this entire control
        # should be blit to the screen canvas
        self.font_small = font_small
        self.font_medium = font_medium  # Medium sized font
        self.font_x_large = font_x_large  # XL sized font
        self.surface = pygame.Surface(
            (int(self.canvas_width + (self.canvas_margin * 2)),
             int(self.canvas_height + (self.canvas_margin * 2))))

    def init_surface(self):
        pass

    def draw_polygon(self, shape, width, color):
        pygame.draw.polygon(self.surface, color, shape.coordinates, width)

    def draw_label_circle(self, shape, labels):
        coord_pair = 0
        for coordinates in shape.coordinates:
            self.draw_label(coordinates,
                            shape.degrees[coord_pair],
                            labels[coord_pair]['noteName'],
                            self.font_medium,
                            self.color)
            coord_pair += 1

    def draw_label(self, coordinates, degrees, text_label, font,
                   color):
        text = font.render(text_label, False, color)
        text = pygame.transform.rotate(text, degrees)
        text_x_center = int(text.get_width() / 2)
        text_y_center = int(text.get_height() / 2)
        # Bit on to the surface:
        self.surface.blit(text, [coordinates[0] - text_x_center,
                                 coordinates[1] - text_y_center])

    def draw_control(self):
        pass

    def update_control(self, events):
        pass


class WheelControl(ControlSystem):
    def __init__(self, *args, **kwargs):
        # Run superclass __init__ to inherit all of those instance attributes
        super(self.__class__, self).__init__(*args, **kwargs)
        self.r = int(self.canvas_height / 2)
        # rotate_offset tracks the overall rotation of the wheel in degrees
        # As the user rotates the wheel, this value is incremented/decremented
        self.rotate_offset = 0

        # rotate_offset_note tracks overall rotation, but for the selected
        # note
        self.rotate_offset_note = 0

        # These are used to track rotation animation of the wheel
        # rotate_steps tracks how many remaining frames of rotation are left
        # to animate for key wheel rotation
        # rotate_iterator will be 1 or -1, and is added to rotate_offset once
        # per cycle until rotate_steps runs out
        self.rotate_steps = 0
        self.rotate_iterator = 0

        # These are used to track rotation animation of the note selection
        # rotate_steps_note tracks how many remaining frames of rotation are
        # left to animate for note selection
        # rotate_iterator_note, same as above but for note selection
        self.rotate_steps_note = 0
        self.rotate_iterator_note = 0

        # rotate_amount is how many degrees to hop per event
        # 1 degree per event makes turning the circle sloooow
        self.rotate_amount = int(360 / 12)
        # rotate_speedup is a multiplier of frames to skip, to make
        # animation super quick.  Factors of 30 will work best
        self.rotate_speedup = 10

        # The circle is divided in to 12 segments
        # But if want a _side_ to be oriented upwards, not a _point_
        # then back it up an additional 1/24th of a circle
        self.offset_degrees = int(-360 / 24)

    def rotate_wheel(self, direction):
        # Set direction to 1 for clockwise rotation
        # Set direction to -1 for counterclockwise rotation
        # It's an integer of degrees added to the overall rotation
        # If this is called and there is no rotation currently, begin
        #   rotation immediately
        if self.rotate_steps == 0:
            self.rotate_steps = int(self.rotate_amount / self.rotate_speedup)
            self.rotate_iterator = direction
            # Set the key index as we turn around
            self.key -= self.rotate_iterator
            if self.key > 11:
                self.key = 0
            if self.key < 0:
                self.key = 11
        else:
            # If we receive a rotate call and are already rotating in that
            #   direction, do nothing.
            # Otherwise, if we receive a rotate call and it's for the opposite
            #   direction, reverse the rotation immediately
            if self.rotate_iterator != direction:
                # Compensate for how far we've already been rotating
                self.rotate_steps = int(self.rotate_amount /
                                        self.rotate_speedup) - \
                                    self.rotate_steps
                # and reverse the rotation
                self.rotate_iterator = direction
                # Set the key index as we turn around
                self.key -= self.rotate_iterator
                if self.key > 11:
                    self.key = 0
                if self.key < 0:
                    self.key = 11

    def rotate_note(self, direction):
        # Set direction to 1 for clockwise rotation
        # Set direction to -1 for counterclockwise rotation
        # It's an integer of degrees added to the overall rotation
        # If this is called and there is no rotation currently, begin
        #   rotation immediately
        if self.rotate_steps_note == 0:
            self.rotate_steps_note = int(self.rotate_amount /
                                         self.rotate_speedup)
            self.rotate_iterator_note = direction
            # Set the selected note index as we turn around
            self.note_selection += self.rotate_iterator_note
            if self.note_selection == 6:
                self.note_selection = 11
                self.rotate_offset_note += 150
            if self.note_selection == 10:
                self.note_selection = 5
                self.rotate_offset_note -= 150
            if self.note_selection > 11:
                self.note_selection = 0
            if self.note_selection < 0:
                self.note_selection = 11
        else:
            # If we receive a rotate call and are already rotating in that
            #   direction, do nothing.
            # Otherwise, if we receive a rotate call and it's for the opposite
            #   direction, reverse the rotation immediately
            if self.rotate_iterator_note != direction:
                # Compensate for how far we've already been rotating
                self.rotate_steps_note = int(self.rotate_amount /
                                             self.rotate_speedup) - \
                                    self.rotate_steps_note
                # and reverse the rotation
                self.rotate_iterator_note = direction
                # Set the selected note index as we turn around
                self.note_selection += self.rotate_iterator_note
                if self.note_selection == 6:
                    self.note_selection = 11
                    self.rotate_offset_note += 150
                if self.note_selection == 10:
                    self.note_selection = 5
                    self.rotate_offset_note -= 150
                if self.note_selection > 11:
                    self.note_selection = 0
                if self.note_selection < 0:
                    self.note_selection = 11
        print("self.rotate_offset_note:", self.rotate_offset_note)

    def update_control(self, events):
        # Handle the dict of events passed in for this update
        for event in events:
            if event == "K_a":
                self.rotate_wheel(1)
            if event == "K_d":
                self.rotate_wheel(-1)
            if event == "K_q":
                self.rotate_note(-1)
            if event == "K_e":
                self.rotate_note(1)
            print("Key:", self.key, ", Note:", self.note_selection)

        # Perform any animation steps needed for this update
        if self.rotate_steps > 0:
            self.rotate_offset += (self.rotate_iterator * self.rotate_speedup)
            self.rotate_steps -= 1

        if self.rotate_steps_note > 0:
            self.rotate_offset_note += (self.rotate_iterator_note *
                                        self.rotate_speedup)
            self.rotate_steps_note -= 1

    def draw_control(self):

        ####################
        # Background stuff #
        ####################

        self.surface.fill(self.color_bg)

        # Key label
        for i in [0]:  # Wheel position 0
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r,
                                    slice_no=i,
                                    canvas_margin=self.canvas_margin)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            "Key",
                            self.font_medium,
                            self.color)

        # Labels for directions
        for i in [1]:  # Wheel position 1
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r,
                                    slice_no=i,
                                    canvas_margin=self.canvas_margin)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            "5ths >",
                            self.font_medium,
                            self.color_accent)
        for i in [11]:  # Wheel position 11
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r,
                                    slice_no=i,
                                    canvas_margin=self.canvas_margin)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            "< 4ths",
                            self.font_medium,
                            self.color_accent)

        # Draw the reference circle
        # This uses self.rotate_offset, so it's a rotating layer
        label_circle = ShapeWheel(canvas_size=self.r * 2,
                                  r=self.r - 56,
                                  slice_no=1,
                                  offset_degrees=self.rotate_offset,
                                  canvas_margin=self.canvas_margin,
                                  label_list=self.notes)
        self.draw_label_circle(label_circle, self.notes)

        # Draw the slices
        for i in [0, 1, 2, 3, 4, 5, 11]:
            # Inner triangles bg color fill
            polygon = ShapeWheelSlice(canvas_size=self.r * 2,
                                      r=self.r - 70,
                                      slice_no=i,
                                      offset_degrees=self.offset_degrees,
                                      canvas_margin=self.canvas_margin)
            self.draw_polygon(polygon, 0, self.color_accent)

            # Outlines
            polygon = ShapeWheelSlice(canvas_size=self.r * 2,
                                      r=self.r - 12,
                                      slice_no=i,
                                      offset_degrees=self.offset_degrees,
                                      canvas_margin=self.canvas_margin)
            self.draw_polygon(polygon, 1, self.color)

        labels = {11: {"step": 4,
                       "triad": "MAJ",
                       "mode": "Lydian"},
                  0: {"step": 1,
                       "triad": "MAJ",
                       "mode": "Ionian"},
                  1: {"step": 5,
                      "triad": "MAJ",
                      "mode": "Mixolydian"},
                  2: {"step": 2,
                      "triad": "min",
                      "mode": "Dorian"},
                  3: {"step": 6,
                      "triad": "min",
                      "mode": "Aeolian"},
                  4: {"step": 3,
                      "triad": "min",
                      "mode": "Phrygian"},
                  5: {"step": 7,
                      "triad": "dim",
                      "mode": "Locrian"},
                 }

        for label in labels:  # The 4
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 170,
                                    slice_no=label,
                                    canvas_margin=self.canvas_margin)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(labels[label]["step"]),
                            self.font_medium,
                            self.color_bg)
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 210,
                                    slice_no=label,
                                    canvas_margin=self.canvas_margin)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(labels[label]["triad"]),
                            self.font_small,
                            self.color_bg)
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 365,
                                    slice_no=label,
                                    canvas_margin=self.canvas_margin)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0]+90,
                            str(labels[label]["mode"]),
                            self.font_small,
                            self.color_bg)

        # Draw the selected note indicator
        polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                r=self.r - 126,
                                slice_no=0,
                                offset_degrees=self.rotate_offset_note,
                                canvas_margin=self.canvas_margin)
        self.draw_label(polygon.coordinates[1],
                        polygon.degrees[0],
                        "^",
                        self.font_x_large,
                            self.color)

class Helm:
    def __init__(self, canvas_width=1920, canvas_height=1080, init_gfx=True):

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
                    if event.key == pygame.K_a:
                        events["K_a"] = True
                    if event.key == pygame.K_d:
                        events["K_d"] = True
                    if event.key == pygame.K_q:
                        events["K_q"] = True
                    if event.key == pygame.K_e:
                        events["K_e"] = True
            for controlSurface in self.controlSurfaces:
                controlSurface.update_control(
                    events)  # update control attributes with a dict of events

            self.clock.tick(60)  # 60 fps

        # If we've reached this point, we've escaped the run: loop.  Quit.
        pygame.quit()


if __name__ == "__main__":
    helm = Helm()
    helm.run()
