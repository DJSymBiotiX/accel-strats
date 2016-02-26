#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import struct
import argparse

from libchip.LIS3DH import LIS3DH
from datetime import datetime
from os import remove
from sys import exit

# Setup GPIO Mode
GPIO.setmode(GPIO.BCM)

# Get GPIO Switch pin position
SWITCH = 18


def main():
    args = parse_args()
    debug = args.debug

    print "LIS3DH Accelerometer Sampling"
    print "Sampling is on when switch is flipped"

    # Setup
    GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    sensor = LIS3DH(debug=debug)
    sample_count = 0
    state = True

    print
    filename = 'data-%s.bin' % datetime.now().strftime("%H%M%S")

    with open(filename, 'wb') as f:
        try:
            while 1:
                switch_state = GPIO.input(SWITCH)
                if state != switch_state:
                    state = switch_state
                    if state:
                        print "Sampling is: On"
                    else:
                        print "Sampling is: Off"

                if switch_state:
                    x = sensor.getX()
                    y = sensor.getY()
                    z = sensor.getZ()
                    s = struct.pack('f' * 3, *(x, y, z))
                    f.write(s)
                    sample_count += 3

                time.sleep(0.01)
        except KeyboardInterrupt:
            pass

    # If sample count is 0 delete the empty file
    print
    if sample_count == 0:
        remove(filename)
        print "No data collected"
    else:
        print "Wrote out file: %s" % filename

    GPIO.cleanup()
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
