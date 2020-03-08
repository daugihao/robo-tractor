import RPi.GPIO as GPIO
import time

from math import sqrt
from accel import convertAcc

from wii import Wiimote

PIN_PNEU1 = 12
PIN_PNEU2 = 13
PIN_ELEC1 = 15
PIN_ELEC2 = 16
PIN_KILLSW = 29
PIN_SPARE2 = 31
PIN_SPARE3 = 33
PIN_SPARE4 = 35

T_CYCLE = 0.1
T_PNEU = 3.0
T_START = 5.0

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(PIN_PNEU1, GPIO.OUT)
GPIO.setup(PIN_PNEU2, GPIO.OUT)
GPIO.setup(PIN_ELEC1, GPIO.OUT)
GPIO.setup(PIN_ELEC2, GPIO.OUT)
GPIO.setup(PIN_KILLSW, GPIO.OUT)
GPIO.setup(PIN_SPARE2, GPIO.OUT)
GPIO.setup(PIN_SPARE3, GPIO.OUT)
GPIO.setup(PIN_SPARE4, GPIO.OUT)
GPIO.output(PIN_PNEU1, GPIO.LOW)
GPIO.output(PIN_PNEU2, GPIO.HIGH)
GPIO.output(PIN_ELEC1, GPIO.HIGH)
GPIO.output(PIN_ELEC2, GPIO.HIGH)
GPIO.output(PIN_KILLSW, GPIO.HIGH)
GPIO.output(PIN_SPARE2, GPIO.HIGH)
GPIO.output(PIN_SPARE3, GPIO.HIGH)
GPIO.output(PIN_SPARE4, GPIO.HIGH)


wiimote = Wiimote()
time.sleep(1)

timer_accel = 0.0
timer_start = 0.0
killed = True

while True:
    time.sleep(T_CYCLE)
    buttons = wiimote.buttons()

    # Control braking pnuematics
    print("trigger: " + str(buttons["trigger"]))
    if buttons["trigger"]:
        timer_brake = 0.0
        timer_accel += T_CYCLE
        if timer_accel > T_PNEU:
            GPIO.output(PIN_PNEU1, GPIO.HIGH)
            GPIO.output(PIN_PNEU2, GPIO.HIGH)
        else:
            GPIO.output(PIN_PNEU1, GPIO.HIGH)
            GPIO.output(PIN_PNEU2, GPIO.LOW)
    else:
        timer_accel = 0.0
        GPIO.output(PIN_PNEU1, GPIO.LOW)
        GPIO.output(PIN_PNEU2, GPIO.HIGH)
    
    # Control steering motor
    print("left: " + str(buttons["left"]))
    print("right: " + str(buttons["right"]))
    if buttons["left"] and not buttons["right"]:
        GPIO.output(PIN_ELEC1, GPIO.LOW)
        GPIO.output(PIN_ELEC2, GPIO.HIGH)
    elif buttons["right"] and not buttons["left"]:
        GPIO.output(PIN_ELEC1, GPIO.HIGH)
        GPIO.output(PIN_ELEC2, GPIO.LOW)
    else:
        GPIO.output(PIN_ELEC1, GPIO.HIGH)
        GPIO.output(PIN_ELEC2, GPIO.HIGH)
    
    # Control kill switch
    if killed:
        GPIO.output(PIN_KILLSW, GPIO.HIGH)
        wiimote.led(9)
    else:
        GPIO.output(PIN_KILLSW, GPIO.LOW)
        wiimote.led(15)

    if buttons["a"]:
        if killed:
            timer_start += T_CYCLE
            if timer_start > T_START:
                killed = False
        else:
            timer_start = 0
            killed = True
    else:
        timer_start = 0
    
    # Control spares
    if buttons["minus"]:
        GPIO.output(PIN_SPARE2, GPIO.LOW)
    else:
        GPIO.output(PIN_SPARE2, GPIO.HIGH)
    if buttons["home"]:
        GPIO.output(PIN_SPARE3, GPIO.LOW)
    else:
        GPIO.output(PIN_SPARE3, GPIO.HIGH)
    if buttons["plus"]:
        GPIO.output(PIN_SPARE4, GPIO.LOW)
    else:
        GPIO.output(PIN_SPARE4, GPIO.HIGH)
