import pygame
import sys
from helm_shapes import ShapeWheel, ShapeWheelRay, ShapeWheelSlice, \
                        ShapeNotesList


class ControlSystem(object):

    key = 0  # Key is the index of the notes dict indicating the key

    def __init__(self, canvas_width, canvas_margin, color,
                 color_bg, color_accent, notes, blit_x, blit_y, font_small,
                 font_medium, font_medium_bold, font_x_large,
                 wheel_control=None):
        self.surface = None
        self.canvas_width = canvas_width
        self.canvas_height = canvas_width  # 1:1 control canvas ratio default
        self.canvas_margin = canvas_margin
        self.color = color
        self.color_bg = color_bg
        self.color_accent = color_accent
        self.notes = notes  # Holds the dict/lists representing the scale
        # notes, their positions and values, etc
        self.chord_position = 0  # The currently selected note position
        self.chord_selection = 0  # Currently selected chord root note index
        self.blit_x = blit_x  # The X location in which this entire control
        # should be blit to the screen canvas
        self.blit_y = blit_y  # The Y location in which this entire control
        # should be blit to the screen canvas
        self.font_small = font_small
        self.font_medium = font_medium  # Medium sized font
        self.font_medium_bold = font_medium_bold
        self.font_x_large = font_x_large  # XL sized font
        self.surface = pygame.Surface(
            (int(self.canvas_width + (self.canvas_margin * 2)),
             int(self.canvas_height + (self.canvas_margin * 2))))

    def init_surface(self):
        pass

    def draw_polygon(self, shape, width, color):
        pygame.draw.polygon(self.surface, color, shape.coordinates, width)

    def draw_key_labels(self, shape, labels, key):
        coord_pair = 0
        for coordinates in shape.coordinates:
            if (coord_pair >= key) and \
               (coord_pair <= (key + 5) ) and \
                    (key in range(7)):
                # sharps
                note_label = labels[coord_pair]['sharpName']
            else:
                note_label = labels[coord_pair]['noteName']
            if key == coord_pair:
                font = self.font_medium_bold
            else:
                font = self.font_medium
            self.draw_label(coordinates,
                            shape.degrees[coord_pair],
                            note_label,
                            font,
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


class ChordControl(ControlSystem):
    def __init__(self, *args, **kwargs):
        # Run superclass __init__ to inherit all of those instance attributes
        super(self.__class__, self).__init__(*args, **kwargs)

        # Reference to a wheelControl to get / set attributes
        self.wheel_control = kwargs.get('wheel_control', None)
        self.canvas_height = 400
        self.surface = pygame.Surface(
            (int(self.canvas_width + (self.canvas_margin * 2)),
             int(self.canvas_height + (self.canvas_margin * 2))))

        # For now, how intervals are defined:
        # The 'slice number' around the circle of fifths
        # 1 = Root
        # 2 = Fifth
        # 3 = Second
        # 4 = Sixth
        # 5 = Third
        # 6 = Seventh
        # 7 = Fourth
        self.chord_slices_dict = {1: 1,
                                  2: 5,
                                  3: 2,
                                  4: 6,
                                  5: 3,
                                  6: 7,
                                  7: 4}
        self.chord_definitions = {'1, 3, 5': (1, 3, 5)
                                  }
        # self.chord_definitions = {'1, 3, 5': (1, 3, 5),
        #                           '1, 3, 5, 6': (1, 3, 5, 6),
        #                           '1, 3, 5, 7': (1, 3, 5, 7),
        #                           '1, 3, 5, 9': (1, 3, 5, 2),
        #                           '1, 3, 5, 7, 9': (1, 3, 5, 7, 2),
        #                           '1, 5, 7, 9, 11': (1, 5, 7, 2, 4)}

    def update_control(self, events):
        # Handle the dict of events passed in for this update
        for event in events:
            if event == "chord_majortriad_start":
                print("major triad on. key:", self.key)
            if event == "chord_majortriad_stop":
                print("major triad off. key:", self.key)

    def draw_squares(self, shape, color, width, chord_root, chord_def):
        # IT'S ALL BAD
        # coord_pair = 0
        # for coordinates in shape.coordinates_boxes:
            # print("coord_pair:",coord_pair)
            # print("self.notes[coord_pair]['wheelPos']:",self.notes[coord_pair]['wheelPos'])
            # print("wheel_control.chord_selection:",self.wheel_control.chord_selection)
            # print("chord_def:",chord_def)
            # if (
            #     (abs(coord_pair - self.wheel_control.chord_selection) % 12)
            # ) in chord_def:
            #     rect = pygame.Rect(coordinates)
            #     pygame.draw.rect(self.surface, color, rect, width)
            #     # print("* draw square on:",coord_pair)
            # coord_pair += 1
        # sys.exit()
        # Starting over
        for i in range(7):
            print("i:", i)
            print("self.wheel_control.key:", self.wheel_control.key)
            print("self.chord_slices_dict[i+1]:", self.chord_slices_dict[i+1])
            print("chord_def:",chord_def)
            if self.chord_slices_dict[i+1] in chord_def:
                current_loc = i + self.wheel_control.chord_selection
                print("self.wheel_control.chord_selection:", self.wheel_control.chord_selection)
                print("current_loc:", current_loc)
                # if (current_loc >= (6 + self.wheel_control.key)) and \
                #         (current_loc < (11 + self.wheel_control.key)):
                if (current_loc >= 6) and \
                        (current_loc < 11):
                    current_loc += 5
                current_slice = (current_loc) % 12
                print("current_slice:", current_slice)
                rect = pygame.Rect(shape.coordinates_boxes[current_slice])
                pygame.draw.rect(self.surface, color, rect, width)
            # sys.exit()

    def draw_control(self):
        self.surface.fill(self.color_bg)

        line_spacing = 0
        for chord_def in self.chord_definitions:
            line_coords = ShapeNotesList(spacing_width=44,
                                         canvas_margin=self.canvas_margin,
                                         line_spacing=line_spacing,
                                         left_margin=226)
            self.draw_squares(line_coords, self.color, 1,
                              self.wheel_control.chord_selection,
                              self.chord_definitions[chord_def])
            self.draw_key_labels(line_coords, self.notes,
                                 self.wheel_control.key)
            self.draw_label((line_coords.coordinates[0][0]-168,
                             line_coords.coordinates[0][1]),
                            0,
                            chord_def,
                            self.font_small, self.color)
            line_spacing += 60


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
        self.rotate_offset_chord = 0

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
        self.rotate_steps_chord = 0
        self.rotate_iterator_chord = 0

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

    # TODO these two methods could be collapsed in to one
    def rotate_wheel(self, direction):
        # Set direction to 1 for clockwise rotation
        # Set direction to -1 for counterclockwise rotation
        # It's an integer of degrees added to the overall rotation
        # If this is called and there is no rotation currently, begin
        #   rotation immediately
        if ( self.rotate_steps == 0 ) or (self.rotate_iterator != direction):
            self.rotate_steps = int(self.rotate_amount / self.rotate_speedup) \
                                    - self.rotate_steps
            self.rotate_iterator = direction
            # Set the key index as we turn around
            # Subtract because of the rotating-disk mechanic, the newly chosen
            # option is OPPOSITE direction of the disk turning
            self.key -= self.rotate_iterator
            # Rollover range 0-11
            self.key = abs(self.key % 12)
            # Change the chord, too
            self.chord_selection -= self.rotate_iterator
            self.chord_selection = abs(self.chord_selection % 12)

    def rotate_chord(self, direction):
        # Set direction to 1 for clockwise rotation
        # Set direction to -1 for counterclockwise rotation
        # It's an integer of degrees added to the overall rotation
        # If this is called and there is no rotation currently, begin
        #   rotation immediately
        # TODO use a dict to track the whole wheel state and all rotate steps
        if (self.rotate_steps_chord == 0) or \
                (self.rotate_iterator_chord != direction):
            self.rotate_steps_chord = int(self.rotate_amount /
                                          self.rotate_speedup) \
                                      - self.rotate_steps_chord
            self.rotate_iterator_chord = direction
            # Set the selected note index as we turn around
            self.chord_position += self.rotate_iterator_chord
            self.chord_position = abs(self.chord_position % 12)
            # Change the chord, too
            self.chord_selection += self.rotate_iterator_chord
            self.chord_selection = abs(self.chord_selection % 12)
            if self.chord_position == 6:
                self.chord_position = 11
                self.chord_selection = abs((11 + self.key) % 12)
                self.rotate_offset_chord += 150
            if self.chord_position == 10:
                self.chord_position = 5
                self.chord_selection = abs((5 + self.key) % 12)
                self.rotate_offset_chord -= 150


    def update_control(self, events):
        # Handle the dict of events passed in for this update
        for event in events:
            if event == "key_clockwise":
                self.rotate_wheel(1)
            if event == "key_counterclockwise":
                self.rotate_wheel(-1)
            if event == "chord_clockwise":
                self.rotate_chord(-1)
            if event == "chord_counterclockwise":
                self.rotate_chord(1)
            print("Key:", self.notes[self.key]['noteName'],
                  ", Mode root:", self.notes[self.chord_selection]['noteName'],
                  ", self.key:", self.key,
                  ", self.chord_selection:", self.chord_selection)

        # Perform any animation steps needed for this update
        if self.rotate_steps > 0:
            self.rotate_offset += (self.rotate_iterator * self.rotate_speedup)
            self.rotate_steps -= 1

        if self.rotate_steps_chord > 0:
            self.rotate_offset_chord += (self.rotate_iterator_chord *
                                         self.rotate_speedup)
            self.rotate_steps_chord -= 1

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
        label_circle = ShapeWheel(r=self.r - 56,
                                  slice_no=1,
                                  offset_degrees=self.rotate_offset,
                                  canvas_margin=self.canvas_margin)
        self.draw_key_labels(label_circle, self.notes, self.key)

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
                                    r=self.r - 200,
                                    slice_no=label,
                                    canvas_margin=self.canvas_margin)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(labels[label]["step"]),
                            self.font_medium_bold,
                            self.color_bg)
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 240,
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
                                offset_degrees=self.rotate_offset_chord,
                                canvas_margin=self.canvas_margin)
        self.draw_label(polygon.coordinates[1],
                        polygon.degrees[0],
                        "^",
                        self.font_x_large,
                            self.color)