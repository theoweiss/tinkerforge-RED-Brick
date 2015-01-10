#!/usr/bin/python
import shutil
import os
import subprocess
import sys
import threading
import time
from tinkerforge.ip_connection import IPConnection
from tinkerforge.bricklet_ambient_light import AmbientLight
from tinkerforge.bricklet_barometer import Barometer
from tinkerforge.bricklet_humidity import Humidity
from tinkerforge.bricklet_lcd_20x4 import LCD20x4

barometerid = None
humidityid = None
ambientid = None
lcdid = None

def installSitemap(srcbase, dstbase):
    sitemapsrc = os.path.join(srcbase, "tf.sitemap")
    sitemapdst = os.path.join(dstbase, "sitemaps", "tf.sitemap")
    shutil.copy(sitemapsrc, sitemapdst)
     
def installRules(srcbase, dstbase):
    rulessrc = os.path.join(srcbase, "tf.rules")
    rulesdst = os.path.join(dstbase, "rules", "tf.rules")
    shutil.copy(rulessrc, rulesdst)

def installItems(srcbase, dstbase, tmp):
    itemsfilename = "tf.items"    
    itemssrc = os.path.join(srcbase, itemsfilename)
    itemstmpfile = os.path.join(tmp, itemsfilename)
    tmpinfh = open(itemssrc, "r") 
    tmpoutfh = open(itemstmpfile, "w")
    humpattern = "%%HUMIDITYID%%"
    barometerpattern = "%%BAROMETERID%%"
    ambientlightpattern = "%%AMBIENTLIGHTID%%"
    lcdpattern = "%%LCDID%%"
    for line in tmpinfh:
        l = line.replace("%%HUMIDITYID%%", humidityid).replace("%%BAROMETERID%%", barometerid).replace("%%AMBIENTLIGHTID%%", ambientid).replace("%%LCDID%%", lcdid)
        tmpoutfh.write(l)
    tmpinfh.close()
    tmpoutfh.close()
    itemsdst = os.path.join(dstbase, "items", itemsfilename)
    shutil.copy(itemstmpfile, itemsdst)
    
def installOpenhabcfg(srcbase, dstbase):
    openhabcfgsrc = os.path.join(srcbase, "openhab.cfg")
    openhabcfgdst = os.path.join(dstbase, "openhab.cfg")
    shutil.copy(openhabcfgsrc, openhabcfgdst)

def restartOpenhab():
    try:
        subprocess.check_output(['/etc/init.d/openhab', 'restart'])
    except subprocess.CalledProcessError, e:
        print "Error : " + e.output
        return e.exitCode
    return 0

def cb_connected(connect_reason):
    ipcon.enumerate()

def cb_enumerate(uid, connected_uid, position, hardware_version, firmware_version,
                 device_identifier, enumeration_type):
    #print("UID: " + uid + ", Enumeration Type: " + str(enumeration_type) + " identifier: " + str(device_identifier))
    if device_identifier == AmbientLight.DEVICE_IDENTIFIER:
        global ambientid
        ambientid = uid
    elif device_identifier == Humidity.DEVICE_IDENTIFIER:
        global humidityid
        humidityid = uid
    elif device_identifier == Barometer.DEVICE_IDENTIFIER:
        global barometerid
        barometerid = uid
    elif device_identifier == LCD20x4.DEVICE_IDENTIFIER:
        global lcdid
        lcdid = uid

def wait():
    while (barometerid is None) or (humidityid is None) or (ambientid is None) or (lcdid is None):
        time.sleep(1)

def discover():
    HOST = "localhost"
    PORT = 4223
    global ipcon
    ipcon = IPConnection()
    ipcon.register_callback(IPConnection.CALLBACK_CONNECTED, cb_connected)
    ipcon.register_callback(IPConnection.CALLBACK_ENUMERATE, cb_enumerate)
    ipcon.connect(HOST, PORT)
    w = threading.Thread(target=wait)
    w.start()
    w.join()
    print("baromenter id: " + str(barometerid))
    print("humidity id: " + str(humidityid))
    print("ambient id: " + str(ambientid))
    print("lcd id: " + str(lcdid))
    
    ipcon.disconnect()

def main(args):    
    discover()
    projdir = os.path.split(os.path.dirname(os.path.realpath(args[0])))[0]
    tmp = os.path.join(projdir, 'tmp')
    srcbase = os.path.join(projdir, "resources", "weatherstation")
    dstbase = os.path.join(os.path.sep, "etc", "openhab", "configurations" )
    installOpenhabcfg(srcbase, dstbase)
    installItems(srcbase, dstbase, tmp)
    installSitemap(srcbase, dstbase)
    installRules(srcbase, dstbase)

    #restartOpenhab()

if __name__ == '__main__':
    main(sys.argv)
