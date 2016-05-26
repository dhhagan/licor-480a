'''
    Read data from a Licor 480A

    Written by David H Hagan, May 2016
'''

import os
import sys
import datetime
import serial
import time

# Config Variables
DEBUG   = True
LOG     = True
FREQ    = 1
LOG_DIR = 'logs'
PORT    = '/dev/ttyUSB0'
BAUD    = 9600
TIMEOUT = 20

class Licor:
    def __init__(self, **kwargs):
        self.port       = kwargs.pop('port', '/dev/ttyUSB0')
        self.baud       = kwargs.pop('baud', 9600)
        self.timeout    = kwargs.pop('timeout', 20)
        self.debug      = kwargs.pop('debug', True)

        self._header    = ','.join()

    def connect(self):
        try:
            self.con = serial.Serial(self.port, self.baud, timeout = self.timeout)
        except Exception as e:
            self.con = None

            return e

        return True

    def read(self):
        data = self.con.readline()

        # Make nice and pretty!

        if self.debug:
            print (data)

    def __repr__(self):
        return "Licor Model 408A"

# Set the filename
filename = 'licor-data-{}'.format(datetime.datetime.now())

# If LOG_DIR is set, change to that directory for log purposes
if LOG_DIR:
    filename = os.path.join(LOG_DIR, filename)

# Connect to the LICOR
try:
    licor = Licor( port = PORT, baud = BAUD, timeout = TIMEOUT, debug = DEBUG )
except Exception as e:
    if DEBUG:
        print ("ERROR: {}".format(e))

    sys.exit("Could not connect to the Licor")

if LOG:
    with open(filename, 'w') as f:
        # Write the headers to a file
        f.write(licor._header)

        while True:
            # Read from the licor
            data = licor.read()

            # Write the data to file
            f.write(data)

            # Sleep for FREQ seconds
            time.sleep(FREQ)

        # Close the file
        f.close()
else:
    while True:
        data = licor.read()

        time.sleep(FREQ)
