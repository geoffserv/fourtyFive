import pygame
from helm_shapes import ShapeWheel, ShapeWheelRay, ShapeWheelSlice, \
                        ShapeNotesList
import helm_globals
import helm_fonts


class ControlSystem(object):

    def __init__(self, **kwargs):
        # Informal interface for a ControlSystem

        # 1:1 control canvas ratio default
        self.canvas_width = kwargs.get('canvas_size', 100)
        self.canvas_height = kwargs.get('canvas_size', 100)

        self.color = kwargs.get('color', helm_globals.color_orange)
        self.color_bg = kwargs.get('color_bg', helm_globals.color_black)
        self.color_accent = kwargs.get('color_accent',
                                       helm_globals.color_orange_25)

        # The X location in which this entire control
        # should be blit to the screen canvas
        self.blit_x = kwargs.get('blit_x', helm_globals.canvas_margin)

        # The Y location in which this entire control
        # should be blit to the screen canvas
        self.blit_y = kwargs.get('blit_y', helm_globals.canvas_margin)

        self.surface = None
        self.surface = pygame.Surface(
            (int(self.canvas_width + (helm_globals.canvas_margin * 2)),
             int(self.canvas_height + (helm_globals.canvas_margin * 2))))

        # If this is true for this control system, the screen will be
        # re-rendered.
        # This will be set to False at the beginning of every execution of the
        #   update_control method.
        # Then, during execution of the update_control method, it will be set
        #   to True if some change is detected which requires a re-render.
        # As we come back around in the main loop, if True is detected here,
        # Everyone gets redrawn.
        # For now, set to True so we get an initial render.
        self.needs_rendering = True

    def init_surface(self):
        pass

    def draw_polygon(self, shape, width, color):
        pygame.draw.polygon(self.surface, color, shape.coordinates, width)

    def draw_key_labels(self, shape, labels, key):
        coord_pair = 0
        for coordinates in shape.coordinates:
            if (coord_pair >= key) and \
               (coord_pair <= (key + 5)) and \
                    (key in range(7)):
                # sharps
                note_label = labels[coord_pair]['sharpName']
            else:
                note_label = labels[coord_pair]['noteName']
            if key == coord_pair:
                font = helm_fonts.font['medium_bold']
            else:
                font = helm_fonts.font['medium']
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
    def __init__(self, **kwargs):
        # Run superclass __init__ to inherit all of those instance attributes
        super(self.__class__, self).__init__(**kwargs)

        self.canvas_height = 400
        self.surface = pygame.Surface(
            (int(self.canvas_width + (helm_globals.canvas_margin * 2)),
             int(self.canvas_height + (helm_globals.canvas_margin * 2))))

    def update_control(self, events):
        self.needs_rendering = False
        # Handle the dict of events passed in for this update
        for event in events:
            if event == "chord_majortriad_start":
                self.needs_rendering = True
                print("major triad on. key:", helm_globals.key)
            if event == "chord_majortriad_stop":
                self.needs_rendering = True
                print("major triad off. key:", helm_globals.key)

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
        # for i in range(7):
        #     print("i:", i)
        #     print("self.wheel_control.key:", self.wheel_control.key)
        #     print("self.chord_slices_dict[i+1]:", self.chord_slices_dict[i+1]
        #     )
        #     print("chord_def:",chord_def)
        #     if self.chord_slices_dict[i+1] in chord_def:
        #         current_loc = i + self.wheel_control.chord_selection
        #         print("self.wheel_control.chord_selection:", self.
        #         wheel_control.chord_selection)
        #         print("current_loc:", current_loc)
        #         # if (current_loc >= (6 + self.wheel_control.key)) and \
        #         #         (current_loc < (11 + self.wheel_control.key)):
        #         if (current_loc >= 6) and \
        #                 (current_loc < 11):
        #             current_loc += 5
        #         current_slice = (current_loc) % 12
        #         print("current_slice:", current_slice)
        #         rect = pygame.Rect(shape.coordinates_boxes[current_slice])
        #         pygame.draw.rect(self.surface, color, rect, width)
        # sys.exit()
        # It's still all awful
        # Just start over dude.
        pass

    def draw_control(self):
        self.surface.fill(self.color_bg)

        line_spacing = 0
        for chord_def in helm_globals.chord_definitions:
            line_coords = ShapeNotesList(spacing_width=44,
                                         line_spacing=line_spacing,
                                         left_margin=226)
            self.draw_squares(line_coords, self.color, 1,
                              helm_globals.chord_selection,
                              helm_globals.chord_definitions[chord_def])
            self.draw_key_labels(line_coords, helm_globals.notes,
                                 helm_globals.key)
            self.draw_label((line_coords.coordinates[0][0]-168,
                             line_coords.coordinates[0][1]),
                            0,
                            chord_def,
                            helm_fonts.font['small_bold'], self.color)
            line_spacing += 60


class WheelControl(ControlSystem):
    def __init__(self, **kwargs):
        # Run superclass __init__ to inherit all of those instance attributes
        super(self.__class__, self).__init__(**kwargs)
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
        if (self.rotate_steps == 0) or (self.rotate_iterator != direction):
            self.rotate_steps = int(self.rotate_amount / self.rotate_speedup) \
                                    - self.rotate_steps
            self.rotate_iterator = direction
            # Set the key index as we turn around
            # Subtract because of the rotating-disk mechanic, the newly chosen
            # option is OPPOSITE direction of the disk turning
            helm_globals.key -= self.rotate_iterator
            # Rollover range 0-11
            helm_globals.key = abs(helm_globals.key % 12)
            # Change the chord, too
            helm_globals.chord_selection -= self.rotate_iterator
            helm_globals.chord_selection = abs(helm_globals.chord_selection
                                               % 12)

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
            helm_globals.chord_position += self.rotate_iterator_chord
            helm_globals.chord_position = abs(helm_globals.chord_position
                                              % 12)
            # Change the chord, too
            helm_globals.chord_selection += self.rotate_iterator_chord
            helm_globals.chord_selection = abs(helm_globals.chord_selection
                                               % 12)
            if helm_globals.chord_position == 6:
                helm_globals.chord_position = 11
                helm_globals.chord_selection = abs((11 + helm_globals.key)
                                                   % 12)
                self.rotate_offset_chord += 150
            if helm_globals.chord_position == 10:
                helm_globals.chord_position = 5
                helm_globals.chord_selection = abs((5 + helm_globals.key)
                                                   % 12)
                self.rotate_offset_chord -= 150

    def update_control(self, events):
        self.needs_rendering = False

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
            print("Key:", helm_globals.notes[helm_globals.key]['noteName'],
                  ", Mode root:",
                  helm_globals.notes[helm_globals.chord_selection]
                  ['noteName'],
                  ", helm_globals.key:",
                  helm_globals.key,
                  ", helm_globals.chord_selection:",
                  helm_globals.chord_selection)

        # Perform any animation steps needed for this update
        if self.rotate_steps > 0:
            self.needs_rendering = True
            self.rotate_offset += (self.rotate_iterator * self.rotate_speedup)
            self.rotate_steps -= 1

        if self.rotate_steps_chord > 0:
            self.needs_rendering = True
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
                                    slice_no=i)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            "Key",
                            helm_fonts.font['medium'],
                            self.color)

        # Labels for directions
        for i in [1]:  # Wheel position 1
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r,
                                    slice_no=i)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            "5ths >",
                            helm_fonts.font['medium'],
                            self.color_accent)
        for i in [11]:  # Wheel position 11
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r,
                                    slice_no=i)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            "< 4ths",
                            helm_fonts.font['medium'],
                            self.color_accent)

        # Draw the reference circle
        # This uses self.rotate_offset, so it's a rotating layer
        label_circle = ShapeWheel(canvas_size=self.r * 2,
                                  r=self.r - 56,
                                  offset_degrees=self.rotate_offset)
        self.draw_key_labels(label_circle, helm_globals.notes,
                             helm_globals.key)

        # Draw the slices
        for i in [0, 1, 2, 3, 4, 5, 11]:
            # Inner triangles bg color fill
            polygon = ShapeWheelSlice(canvas_size=self.r * 2,
                                      r=self.r - 70,
                                      slice_no=i,
                                      offset_degrees=self.offset_degrees)
            self.draw_polygon(polygon, 0, self.color_accent)

            # Outlines
            polygon = ShapeWheelSlice(canvas_size=self.r * 2,
                                      r=self.r - 12,
                                      slice_no=i,
                                      offset_degrees=self.offset_degrees)
            self.draw_polygon(polygon, 1, self.color)

        for label in helm_globals.note_wheel_labels:
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 200,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(helm_globals.note_wheel_labels[label]
                                ["step"]),
                            helm_fonts.font['medium_bold'],
                            self.color_bg)
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 240,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0],
                            str(helm_globals.note_wheel_labels[label]
                                ["triad"]),
                            helm_fonts.font['small_bold'],
                            self.color_bg)
            polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                    r=self.r - 365,
                                    slice_no=label)
            self.draw_label(polygon.coordinates[1],
                            polygon.degrees[0]+90,
                            str(helm_globals.note_wheel_labels[label]
                                ["mode"]),
                            helm_fonts.font['small_bold'],
                            self.color_bg)

        # Draw the selected note indicator
        polygon = ShapeWheelRay(canvas_size=self.r * 2,
                                r=self.r - 126,
                                slice_no=0,
                                offset_degrees=self.rotate_offset_chord)
        self.draw_label(polygon.coordinates[1],
                        polygon.degrees[0],
                        "↑",
                        helm_fonts.font['x_large'],
                        self.color)
