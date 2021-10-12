import mido
import helm_globals


class Midi(object):
    def __init__(self):
        self.inport_name = 'wavestate 1 Out'
        self.outport_name = 'wavestate 1 In'

        self.channel = 0

        if helm_globals.using_midi:
            print("Inports:")
            print(mido.get_output_names())  # To list the output ports
            print("Outports:")
            print(mido.get_input_names())  # To list the input ports
            self.inport = mido.open_input(self.inport_name, autoreset=True)
            self.outport = mido.open_output(self.outport_name, autoreset=True)

        self.octave = 2

        # c0 = 24
        self.c0_offset = 24

    def notes_on(self, notes):
        print("notes_on:", notes)
        if helm_globals.using_midi:
            for note in notes:
                midi_note = helm_globals.key.notes[note]['kbNum'] + \
                            self.c0_offset + (12 * self.octave)
                print("  -on:", midi_note)
                msg = mido.Message('note_on',
                                   channel=self.channel,
                                   note=midi_note,
                                   velocity=100)  # 1 - 127
                self.outport.send(msg)

    def notes_off(self, notes):
        print("notes_off:", notes)
        if helm_globals.using_midi:
            for note in notes:
                midi_note = helm_globals.key.notes[note]['kbNum'] + \
                            self.c0_offset + (12 * self.octave)
                print("  -off:", midi_note)
                msg = mido.Message('note_off',
                                   channel=self.channel,
                                   note=midi_note,
                                   velocity=0)  # 1 - 127
                self.outport.send(msg)
