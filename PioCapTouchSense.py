import time
import machine
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW, autopull=False, pull_thresh=32, autopush=False, push_thresh=32)
def detectTouch():                                         # type: ignore
    pull(block)                 # Get charge delay val     # type: ignore
    mov(x,osr)                  # Load charge delay val    # type: ignore
    wrap_target()               # Only do the above once   # type: ignore
    mov(y, invert(null))        # Set Y to Large (All Ones)# type: ignore
    set(pins, 1)                # Start Charging           # type: ignore
    label("innerloop")                                     # type: ignore
    jmp(pin, "loopescape")      # If Pin is High, Escape   # type: ignore
    jmp(y_dec, "innerloop")     # Loop and decrement Y     # type: ignore
    label("loopescape")                                    # type: ignore
    mov(isr,y)                  # Move Y to Output SR      # type: ignore
    set(pins, 0)                # Discharge                # type: ignore
    push(noblock)               # Push Y                   # type: ignore
    mov(y,x)                    # Load charge delay val    # type: ignore
    label("chargeloop")                                    # type: ignore
    jmp(y_dec, "chargeloop")     # If !Zero, X-- and loop  # type: ignore
    wrap()                                                 # type: ignore

# Turn off internal pull up on jmp pin, will overwhelm 10 MOhm
sense = machine.Pin(12, mode=machine.Pin.IN, pull=None)
# Create the State Machine, a 1 MegaOhm resistor from set_base pin to jmp_pin is needed
sm = rp2.StateMachine(0, detectTouch, freq=125_000_000, set_base=machine.Pin(9), jmp_pin=machine.Pin(12))

# Start the State Machine.
sm.active(1)

sm.put(1_250_000, 0)  #This sets Charging Delay and detection rate (10 ms)

baseline = 3_000_000 # Inital IIR Value for touch detection
DATA_IIR_CONST = 1_000  # Filtering constant for the baseline capacitance
last_touch = time.ticks_ms() # Limit immediate and back-to-back touch detections
touch_sensitivity = 2_000_000 # Cap dependent
back_to_back_touch_delay_ms = 1000

while True:
    curval = 4_294_967_295 - sm.get() #State Machine counts down from 2^32
    if (curval > baseline + touch_sensitivity) and time.ticks_diff(time.ticks_ms(), last_touch) > back_to_back_touch_delay_ms:
        print("Touch")
        last_touch = time.ticks_ms()
    else:
        baseline = curval / DATA_IIR_CONST + baseline * (DATA_IIR_CONST - 1) / DATA_IIR_CONST
