# helm
A circle of fifths organized python/pygame MIDI instrument.

## Proof-of-concept quality
Pushing towards an operational prototype to see if the idea is fruitful, produces interesting output, should proceed down a different direction, etc.
Everything is bad and hacky but I'll improve as I go and need.

## Concept
- Starting with a circle of fifths, the key is C and the mode root is C
- User is able to rotate the key clockwise and counterclockwise,
- And also rotate the mode root clockwise and counter clockwise.
- Then trigger one of either six predefined chord formulas, as well as the single root note alone
- The host computer will be attached to a USB MIDI device, and will send the appropriate MIDI messages to the USB MIDI device

[![helm](https://github.com/geoffserv/helm/actions/workflows/push_pr.yml/badge.svg?branch=master&event=push)](https://github.com/geoffserv/helm/actions/workflows/push_pr.yml) latest push to `master`.
