'''
    Read data from a Licor 480A

    Written by David H Hagan, May 2016

'''

import os
import sys
import datetime
import serial
import time
from bs4 import BeautifulSoup as bs

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

        self._header    = [
                            'timestamp',
                            'cell_temp',
                            'cell_pressure',
                            'co2',
                            'co2_abs',
                            'h20',
                            'h20_abs',
                            'h20_dewpoint',
                            'ivolt',
                            'raw_co2',
                            'raw_co2_ref',
                            'raw_h20',
                            'raw_h20_ref']

    def connect(self):
        try:
            self.con = serial.Serial(self.port, self.baud, timeout = self.timeout)
        except Exception as e:
            self.con = None

            return e

        return True

    def read(self):
        # Convert to xml using BeautifulSoup
        raw = bs(self.con.readline(), 'lxml')

        # Make nice and pretty!
        raw = raw.li840

        res = [
            datetime.datetime.now().isoformat(),
            raw.data.celltemp.string,
            raw.data.cellpres.string,
            raw.data.co2.string,
            raw.data.co2abs.string,
            raw.data.h2o.string,
            raw.data.h2oabs.string,
            raw.data.h2odewpoint.string,
            raw.data.ivolt.string,
            raw.data.raw.co2.string,
            raw.data.raw.co2ref.string,
            raw.data.raw.h2o.string,
            raw.data.raw.h2oref.string
            ]

        if self.debug:
            print ("\nNew Data Point")
            for each in zip(self._header, res):
                print (each[0], each[1])

        return res

    def __repr__(self):
        return "Licor Model 408A"

# Set the filename
filename = 'licor-data-{}.csv'.format(datetime.datetime.now())

# If LOG_DIR is set, change to that directory for log purposes
if LOG_DIR:
    filename = os.path.join(LOG_DIR, filename)

# Connect to the LICOR
try:
    licor = Licor( port = PORT, baud = BAUD, timeout = TIMEOUT, debug = DEBUG )
    licor.connect()
except Exception as e:
    if DEBUG:
        print ("ERROR: {}".format(e))

    sys.exit("Could not connect to the Licor")

if LOG:
    with open(filename, 'w') as f:
        # Write the headers to a file
        f.write(','.join(licor._header))
        f.write('\n')

        while True:
            # Read from the licor
            data = licor.read()

            # Write the data to file
            f.write(','.join(data))
            f.write('\n')

            # Sleep for FREQ seconds
            time.sleep(FREQ)

        # Close the file
        f.close()
else:
    while True:
        data = licor.read()

        time.sleep(FREQ)
