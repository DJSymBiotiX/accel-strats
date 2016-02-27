#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import struct
import argparse
import signal

from libchip.LIS3DH import LIS3DH
from datetime import datetime
from os import remove, stat, kill, getpid, path
from sys import exit, stdout
from threading import Event

from mailhelper import mail
from graph import make_graph


from settings import (
    GPIO_MODE_BOARD,
    SWITCH,
    STATUS_LED,
    NOTIFY_EMAIL,
    DATA_DIRECTORY,
)

class Globals:
    State = False
    SwitchState = False


def output_state():
    if STATUS_LED is None:
        return
    if Globals.State:
        GPIO.output(STATUS_LED, GPIO.HIGH)
        print
        print "Samping is: on"
    else:
        GPIO.output(STATUS_LED, GPIO.LOW)
        print
        print "Samping is: off"

def switch_down(pin):
    # Interrupt handling routine for when the switch is pressed,
    # sends SIGUSR1 to the process which allows it to wake up from the
    # earlier sleep (signal.pause).
    # This is awkward but seems to be necessary to keep KeyboardInterrupts
    # working when using interrupt and a non polling approach with RPi GPIO
    kill(getpid(), signal.SIGUSR1)

def toggle_state(signal, frame):
    # Do the state transition after  SIGUSR1 comes in
    Globals.State = not Globals.State
    output_state()

def take_sample(f, sensor):
    x = sensor.getX()
    y = sensor.getY()
    z = sensor.getZ()
    s = struct.pack('f' * 3, *(x, y, z))
    f.write(s)


def take_samples(sensor):
    sample_count = 0
    filename = 'data-%s.bin' % datetime.now().strftime("%Y%m%d-%H%M%S")
    filepath = path.join(DATA_DIRECTORY, filename)
    print "Trying to collect samples in %s:" % filename
    with open(filepath, 'wb') as f:
        while Globals.State:
            take_sample(f, sensor)
            sample_count += 1
            if sample_count % 100 == 0:
                stdout.write(".")
                stdout.flush()
            time.sleep(0.01)
        print

    # If the file is empty, delete it
    samples = stat(filepath).st_size / 4
    print
    if samples == 0:
        print "No data collected"
        remove(filepath)
    else:
        print "Wrote out %d samples to %s" % (samples, filename)
        pngpath = filepath[:-3] + 'png'
        print "Making %s" % pngpath,
        make_graph(filepath, pngpath)
        print "Done"
        print "Sending mail to %s.." % NOTIFY_EMAIL,
        mail(
            NOTIFY_EMAIL,
            "Report - %s" % filename,
            "Got %d samples for file %s" % (samples, filename),
            attach=filepath, image=pngpath
        )
        print "Done"


def main():
    args = parse_args()
    debug = args.debug

    print "LIS3DH Accelerometer Sampling"
    print "Sampling is on when switch is flipped"
    print

    sensor = LIS3DH(debug=debug)
    signal.signal(signal.SIGUSR1, toggle_state)

    if GPIO_MODE_BOARD:
        GPIO.setmode(GPIO.BOARD)
    else:
        GPIO.setmode(GPIO.BCM)

    try:
        # Setup
        GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        if STATUS_LED is not None:
            GPIO.setup(STATUS_LED, GPIO.OUT, initial=GPIO.LOW)


        GPIO.add_event_detect(SWITCH, GPIO.RISING, callback=switch_down,
                bouncetime=1000)

        while 1:
            print "Waiting for button press"
            signal.pause()
            print "Button pressed, activating"
            take_samples(sensor)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()

    print "Done"

    exit(0)


def parse_args():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description='graph accelerometer data'
    )

    # Optional Arguments
    parser.add_argument(
        '-d', '--debug', action="store_true",
        help='enable debug mode'
    )

    return parser.parse_args()


if __name__ == "__main__":
    main()
