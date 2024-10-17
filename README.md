# RaspPiPicoTouchSensor
Capacitive Touch Sensing using a Raspberry Pi Pico PIO State Machine

## How it Works
This code uses a PIO state machine to repeatadly charge via an output pin and 1 MegaOhm resistor and detect a change in capacitance on the input pin.  The charge time is set by an inital value written in scratch register X, as the PIO SET instruction is limited to 31.  The statemachine then sets Y to all ones, sets the charge pin to "1", and counts down until the input (jump pin) goes low.  The value is outputted, the charge pin is set to discharge "0", and then the discharge delay is performed.

The userspace code calibrates the baseline charge time with an IIR filter, and if a difference (here 500 cyles or 4 us) in the charge time is detected a touch even is registered.  The touch detection is debounced via a time delay gate, as a single human touch event can trigger multiple detections.

## Improvements
Work in progress (PioCapTouchSenseOpt.py)


-Use sideset to toggle charge pin (Saves 2 instructions)
-Modify such that the charge delay can be loaded from a set (Saves another 2 instructions)
    - Hard to do at full speed, a set(1) reversed is still over a second (2^27 / 125 MHz)
    - Assuming 1 pin sideset, an unreversed loop with a delay of 15 ms can be achieved with a clock divider of 4096 0.24 s (max set: 31 * max delay: 15 * max clock divider:4095 / 125 MHz)
