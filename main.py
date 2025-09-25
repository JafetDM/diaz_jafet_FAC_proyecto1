import machine
import time

led = machine.Pin("LED", machine.Pin.OUT)

sw420 = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

while True:
    if (sw420.value() == 1):
        led.value(1)
        time.sleep(0.5)
    else:
        led.value(0)



