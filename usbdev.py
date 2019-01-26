from pyudev import Context, Monitor, MonitorObserver
import os


#some globals for the device details
USBDEV_UUID = None
USBDEV_VENDOR = None
USBDEV_SERID = None
USBDEV_FSTYPE = None
USBDEV_MODEL = None

USBDEV_HAVEDATA = True


#callback when a usb device is plugged in
def usbEventCallback(action, device):

    global USBDEV_UUID
    global USBDEV_VENDOR
    global USBDEV_SERID
    global USBDEV_FSTYPE
    global USBDEV_MODEL


    global USBDEV_HAVEDATA
    
    if action == 'add':
        #store the device values
        USBDEV_VENDOR = device.get('ID_VENDOR')
        USBDEV_SERID = device.get('ID_SERIAL')
        USBDEV_UUID = device.get('ID_FS_UUID')
        USBDEV_FSTYPE = device.get('ID_FS_TYPE')
        USBDEV_MODEL = device.get('ID_MODEL')
        USBDEV_HAVEDATA = True

    elif action == 'remove':
        #clear the device data
        USBDEV_VENDOR = None
        USBDEV_SERID = None
        USBDEV_UUID = None
        USBDEV_FSTYPE = None
        USBDEV_MODEL = None
        USBDEV_HAVEDATA = False



def startListener():
    # create a context, create monitor at kernel level, select devices
    context = Context()
    monitor = Monitor.from_netlink(context)
    monitor.filter_by(subsystem='block')

    observer = MonitorObserver(monitor, usbEventCallback, name="usbdev")
    #set this as the main thread
    observer.setDaemon(False)
    observer.start()

    return observer

def isDeviceConnected():
    global USBDEV_HAVEDATA
    return USBDEV_HAVEDATA

def getDevData():
    if isDeviceConnected():
        global USBDEV_UUID
        global USBDEV_VENDOR
        global USBDEV_SERID
        global USBDEV_FSTYPE
        global USBDEV_MODEL
        return {'UUID': USBDEV_UUID,
               'SERID': USBDEV_SERID, 
               'VENDOR': USBDEV_VENDOR, 
               'FSTYPE': USBDEV_FSTYPE,
               'MODEL': USBDEV_MODEL}
    return None

def stopListening(observer):
    observer.stop()


#returns the accesible path of the device on the Raspberry pi
#you can change how the path gets calulated.
def getMountPathUsbDevice():
    global USBDEV_UUID
    if not isDeviceConnected() or USBDEV_UUID == None:
        return None
    
    path = os.path.join("~/../../media/pi/", USBDEV_UUID)
    return path

