import pygame
from helm_shapes import ShapeWheel, ShapeWheelRay, ShapeWheelSlice


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