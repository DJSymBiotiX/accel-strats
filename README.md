accel-strats
============

Use the LIS3DH breakout board to detect acceleration and write it out to a file

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
  * Connect a switch to GPIO #18 on the pi (pin 12) to 3v3

Run
===

 * Run the software
```
    sudo python accel.py
```

