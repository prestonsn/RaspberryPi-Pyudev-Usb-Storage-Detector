# RaspberryPi-Pyudev-Usb-Storage-Detector
A module to find a USB storage device on the Raspberry Pi which includes methods to get the mount directory and other information from the USB device. Since this is a wrapper over pyudev, pyudev must first be installed.

Example Usage:
```Python

import usbdev
import time

#start listening for usb device change events
#you may have to unplug the flashdrive and replug
usbdev.startListener()

while 1:
    time.sleep(1)

    #get the status of the connected usb device
    status = usbdev.isDeviceConnected()

    #get some identification data 
    #returns a dict with keys UUID, SERID (for serial ID), 
    #VENDOR (the manufacturer), FSTYPE (file system), MODEL (the model).
    device = usbdev.getDevData()

    #get the path (currently set for Rpi, can be changed)
    path = usbdev.getMountPathUsbDevice()

    print("Stat: " + str(status))
    print("dev: " + str(device))
    print("path: " + str(path))
    print("---------------------------------")
```

Example output:
