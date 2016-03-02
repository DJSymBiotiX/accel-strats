accel-strats
============

Script to collect data with the LIS3DH breakout board.

Connects to a status led and momentary switch over GPIO.

When collection is off, pressing the switch results in:

 * Status LED turning on
 * Collection turns on and begins writing to a binary file

When collection is on, pressing the switch results in:

 * Status LED turning off
 * Collection stops
 * Any written data is graphed using matplotlib
 * The data file and the png graph are emailed to you using gmail

Attribution
===========

 * LIS3DH.py - https://github.com/mattdy/python-lis3dh
 * Adafruit\_I2C - https://github.com/adafruit/Adafruit-Raspberry-Pi-Python-Code

Setup
=====

 * Install the smbus and i2c tools onto the pi
```
    sudo apt-get install python-smbus
    sudo apt-get install i2c-tools
```

 * Install kernel support with raspi-config
```
    sudo raspi-config
```
  * Go to "Advanced Options"
  * Enable I2C
  * Reboot

 * Install requirements
```
    pip install -r requirements.txt
```

 * Connect the proper cables
  * LIS3DH Breakout -> Raspberri Pi:
   * Vin -> 3v3
   * GND -> GND
   * SDA -> SDA
   * SCL -> SCL

  * Connect a momentary switch to GPIO
  * Connect a status LED to GPIO
  * Make a settings file

    cp settings_sample.py settings.py
    vi settings.py

Run
===

 * Run the software manually

    sudo python accel.py

 * Run it in tmux at boot with the following cronjob

    @reboot /path/to/this/project/startup.sh


```

