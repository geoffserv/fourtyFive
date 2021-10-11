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

# Musical attributes
notes = [
    {'noteName': 'C', 'sharpName': 'C', 'kbNum': 1, 'wheelPos': 1},
    {'noteName': 'G', 'sharpName': 'G', 'kbNum': 8, 'wheelPos': 2},
    {'noteName': 'D', 'sharpName': 'D', 'kbNum': 3, 'wheelPos': 3},
    {'noteName': 'A', 'sharpName': 'A', 'kbNum': 10, 'wheelPos': 4},
    {'noteName': 'E', 'sharpName': 'E', 'kbNum': 5, 'wheelPos': 5},
    {'noteName': 'B', 'sharpName': 'B', 'kbNum': 12, 'wheelPos': 6},
    {'noteName': 'Gb', 'sharpName': 'F#', 'kbNum': 7, 'wheelPos': 7},
    {'noteName': 'Db', 'sharpName': 'C#', 'kbNum': 2, 'wheelPos': 8},
    {'noteName': 'Ab', 'sharpName': 'G#', 'kbNum': 9, 'wheelPos': 9},
    {'noteName': 'Eb', 'sharpName': 'D#', 'kbNum': 4, 'wheelPos': 10},
    {'noteName': 'Bb', 'sharpName': 'A#', 'kbNum': 11, 'wheelPos': 11},
    {'noteName': 'F', 'sharpName': 'E#', 'kbNum': 6, 'wheelPos': 12}
]

key = 0  # Key is the index of the notes dict indicating the key

# notes, their positions and values, etc
chord_position = 0  # The currently selected note position on the circle

chord_selection = 0  # Currently selected chord root note index

# For now, how intervals are defined:
# The 'slice number' around the circle of fifths
# 1 = Root
# 2 = Fifth
# 3 = Second
# 4 = Sixth
# 5 = Third
# 6 = Seventh
# 7 = Fourth
chord_slices_dict = {1: 1,
                          2: 5,
                          3: 2,
                          4: 6,
                          5: 3,
                          6: 7,
                          7: 4}
chord_definitions = {'1, 3, 5': (1, 3, 5)
                          }
# self.chord_definitions = {'1, 3, 5': (1, 3, 5),
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