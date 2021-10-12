# Griffin Powermate support for Linux systems only
# Can't install the dependency evdev unless running linux, because
# part of the install process checks for kernel header files and so on.
# If in linux, set to True and connect a Powermate.  pip install pypowermate
# Make sure to add the current, non-root UNIX user to the input group
# in /etc/group, and then re-login.  Otherwise: permission errors.
# Win / Mac: set to False and no powermate for you :c
using_griffin_powermate = False

# If I try to render things like text, corners of polygons, etc right up
# against the edge of a surface, then there is often clipping.  So, track
# a global canvas_margin to offset all coordinate systems and give some
# empty space around the edges of each surface.
# Define a default canvas_margin:
canvas_margin = 10

# Labels used around the circle
note_wheel_labels = {11: {"step": 4,
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


class Key(object):
    def __init__(self):
        self.current_key = 0
        self.current_chord_root = 0
        self.current_key_mode = 0
        self.notes_on = []  # List containing key.notes indices currently
        # playing 0-11

        self.notes = [
            {'noteName': 'C', 'sharpName': 'C', 'kbNum': 0},
            {'noteName': 'G', 'sharpName': 'G', 'kbNum': 7},
            {'noteName': 'D', 'sharpName': 'D', 'kbNum': 2},
            {'noteName': 'A', 'sharpName': 'A', 'kbNum': 9},
            {'noteName': 'E', 'sharpName': 'E', 'kbNum': 4},
            {'noteName': 'B', 'sharpName': 'B', 'kbNum': 11},
            {'noteName': 'Gb', 'sharpName': 'F#', 'kbNum': 6},
            {'noteName': 'Db', 'sharpName': 'C#', 'kbNum': 1},
            {'noteName': 'Ab', 'sharpName': 'G#', 'kbNum': 8},
            {'noteName': 'Eb', 'sharpName': 'D#', 'kbNum': 3},
            {'noteName': 'Bb', 'sharpName': 'A#', 'kbNum': 10},
            {'noteName': 'F', 'sharpName': 'E#', 'kbNum': 5}
                    ]

        self.diatonic = [0, 1, 2, 3, 4, 5, 11]
        self.chord_scale = [0, 1, 2, 3, 4, 5, 11]
        self.key_scale_ordered = [0, 2, 4, 11, 1, 3, 5]

    def update_diatonic(self):
        self.diatonic = []
        for i in [0, 1, 2, 3, 4, 5, 11]:
            self.diatonic.append(
                (self.current_key + i) % 12
            )
        print("Diatonic: ", self.diatonic)
        print("Diatonic Notes: ", end="")
        for note in self.diatonic:
            print(self.notes[note]['noteName'], end=", ")
        print("")

    def update_chord_scale(self):
        self.chord_scale = []
        for i in range(self.current_key_mode, self.current_key_mode + 7):
            self.chord_scale.append(self.diatonic[i % 7])
        print("Chord Scale: ", self.chord_scale)
        print("Chord Scale Notes: ", end="")
        for note in self.chord_scale:
            print(self.notes[note]['noteName'], end=", ")
        print("")

    def rotate_key(self, add_by=0):
        self.current_key += add_by
        self.current_key = self.current_key % 12  # Rollover range 0-11
        self.update_diatonic()

    def rotate_key_mode(self, add_by=0):
        self.current_key_mode += add_by
        self.current_key_mode = self.current_key_mode % 7

    def rotate_chord(self, add_by=0, set_to=None):
        print("* chord - add_by:", add_by, " self.current_chord_root:",
              self.current_chord_root, " self.current_key_mode:",
              self.current_key_mode)
        self.current_chord_root += add_by
        print("* chord - added now self.current_chord_root:",
              self.current_chord_root)

        if set_to is not None:
            self.current_chord_root = set_to

        self.current_chord_root = self.current_chord_root % 12  # Rollover ...
        print("* chord - mod 12 self.current_chord_root:",
              self.current_chord_root)

        self.update_chord_scale()

    def calculate_chord(self, chord_def):
        chord = []
        for note in chord_def:
            print("self.chord_scale[note]:",
                  self.chord_scale[chord_slices_dict[note]])
            chord.append(self.chord_scale[chord_slices_dict[note]])
        print("chord:", chord)
        return chord


key = Key()

# For now, how intervals are defined:
# The 'slice number' around the circle of fifths
# 0 = Root
# 1 = Fifth
# 2 = Second
# 3 = Sixth
# 4 = Third
# 5 = Seventh
# 6 = Fourth
chord_slices_dict = {1: 0,
                     2: 2,
                     3: 4,
                     4: 6,
                     5: 1,
                     6: 3,
                     7: 5}

chord_definitions = {'1': (1, ),
                     '1, 5': (1, 5),
                     '1, 3, 5': (1, 3, 5),
                     '1, 5, 7': (1, 5, 7),
                     '5, 9': (5, 2),
                     '1, 5, 11': (1, 5, 4)}
# chord_definitions = {'1, 3, 5': (1, 3, 5),
#                           '1, 3, 5, 6': (1, 3, 5, 6),
#                           '1, 3, 5, 7': (1, 3, 5, 7),
#                           '1, 3, 5, 9': (1, 3, 5, 2),
#                           '1, 3, 5, 7, 9': (1, 3, 5, 7, 2),
#                           '1, 5, 7, 9, 11': (1, 5, 7, 2, 4)}


# Define some colors for convenience and readability
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_red = (255, 0, 0)
color_orange = (255, 94, 19)
color_orange_25 = (64, 23, 4)
color_orange_50 = (128, 47, 9)
color_orange_75 = (191, 69, 13)
