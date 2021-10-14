import mido
import helm_globals


class Midi(object):
    def __init__(self):
        self.inport_clock_name = 'wavestate:wavestate MIDI 1 20:0'
        self.inport_name = 'wavestate:wavestate MIDI 1 20:0'
        self.outport_name = 'wavestate:wavestate MIDI 1 20:0'

        self.channel = 0

        if helm_globals.using_midi:
            print("Inports:")
            print(mido.get_output_names())  # To list the output ports
            print("Outports:")
            print(mido.get_input_names())  # To list the input ports
            self.inport = mido.open_input(self.inport_name, autoreset=True)
            self.outport = mido.open_output(self.outport_name, autoreset=True)
            if helm_globals.using_midi_clock:
                self.inport_clock = \
                    mido.open_input(self.inport_clock_name, autoreset=True)
        self.octave = 2

        # c0 = 24
        self.c0_offset = 24

        # Prior fired notes, help send offs to prior selected notes when
        # the keys have been held
        self.notes_prior = []

        # Store prior latched notes so we can turn them off when starting
        # a new chord
        self.notes_latched = []

    def latch(self):
        if helm_globals.notes_latched:
            for note in helm_globals.key.notes_on:
                print("latched:", note)
                self.notes_latched.append(note)

    def notes_trigger(self, mode="off", notes=None):
        # Notes is arriving as form of key.notes index list
        print("mode:", mode, "notes:", notes)

        if (mode == "on") and len(self.notes_latched) > 0:
            self.notes_trigger(mode="off", notes=self.notes_latched)
            print("unlatching:", self.notes_latched)
            self.notes_latched = []

        for note in notes:
            # Calculate 'real' midi note number by adding c0 offset,
            # octave offset, and using 'kbNum' entry in key.notes
            midi_note = helm_globals.key.notes[note]['kbNum'] + \
                        self.c0_offset + (12 * self.octave)
            print("  -midi_note:", midi_note)
            mido_message = "note_off"
            velocity = 0
            if mode == "on":
                mido_message = "note_on"
                velocity = 100

            # Assume there is no action to be taken
            fire = False

            # Send a MIDI message if the mode is "on" and this
            # note isn't already currently playing:
            if (mode == "on") and note not in helm_globals.key.notes_on:
                fire = True
                helm_globals.key.notes_on.append(note)

            # Send a MIDI message if the mode is "off" and this
            # note is already currently playing:
            if (mode == "off") and note in helm_globals.key.notes_on:
                fire = True
                helm_globals.key.notes_on.remove(note)

            if fire:
                print("***** FIRED MESSAGE OVER MIDI *****")
                if helm_globals.using_midi:
                    msg = mido.Message(mido_message,
                                       channel=self.channel,
                                       note=midi_note,
                                       velocity=velocity)  # 1 - 127
                    self.outport.send(msg)



