# RaspPiPicoTouchSensor
Capacitive Touch Sensing using a Raspberry Pi Pico PIO State Machine

## How it Works
This code uses a PIO state machine to repeatadly charge via an output pin and 1 MegaOhm resistor and detect a change in capacitance on the input pin.  The charge time is set by an inital value written in scratch register X, as the PIO SET instruction is limited to 31.  The statemachine then sets Y to all ones, sets the charge pin to "1", and counts down until the input (jump pin) goes low.  The value is outputted, the charge pin is set to discharge "0", and then the discharge delay is performed.

The userspace code calibrates the baseline charge time with an IIR filter, and if a difference (here 500 cyles or 4 us) in the charge time is detected a touch even is registered.  The touch detection is debounced via a time delay gate, as a single human touch event can trigger multiple detections.
