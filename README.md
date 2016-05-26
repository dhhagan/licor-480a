# Licor 480A Logging Script

Python script to log data continuously from a Licor 480A

## Installation

    git clone https://github.com/dhhagan/licor-480.git
    
## Usage

This script can be run from the command line as follows:

    python3 licor.py
    
It can also be set to auto-run by setting up a cronjob.

### Config Variables

Config variables are set at the top of the licor.py file

  * DEBUG: If True, data will be printed to the console
  * LOG: If set True, data will be logged to a csv file
  * FREQ: Sampling/Logging frequency in Seconds (i.e. FREQ = 1, sample every second)
  * LOG_DIR: The log directory can be set, but will default to the operating directory
  * PORT: Port where the Licor is connected (default is '/dev/ttyUSB0')
  * BAUD: Baud rate (default set to 9600)
  * TIMEOUT: Timeout for the serial connection (default set to 20 sec)
