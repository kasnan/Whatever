'''
sudo apt-get install python-pip
sudo pip install pynmea2
sudo apt-get install gpsd gpsd-clients python-gps minicom

sudo nano /boot/cmdline.txt
-> dwc_otg.lpm_enable=0 console=tty1 root=/dev/mmcblk0p2 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait quiet splash plymouth.ignore-serial-consoles

sudo nano /boot/config.txt
->
dtparam=spi=on
dtoverlay=pi3-disable-bt
core_freq=250
enable_uart=1
force_turbo=1
init_uart_baud=9600

stty -F /dev/ttyAMA0 9600
sudo killall gpsd

sudo nano /etc/default/gpsd
->DEVICES="/dev/ttyAMA0"

sudo systemctl enable gpsd.socket
sudo systemctl start gpsd.socket 
sudo cgps -s

-test-
cat /dev/ttyAMA0
or
cgps -s
'''
import serial
import pynmea2
def parseGPS(str):
    if str.find('GGA') > 0:
        msg = pynmea2.parse(str)
        print("Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" %(msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units))

def setPort():
    serialPort = serial.Serial("/dev/ttyAMA0", 9600, timeout=0.5)

def readPos():
    str = serialPort.readline()
    parseGPS(str)
