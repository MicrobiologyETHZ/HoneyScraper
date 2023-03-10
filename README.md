# HoneyScraper
Python Script that accesses the Honeywell Midas Gas Detector periodically and writes the information to a csv file.

## Installation
```
git clone https://github.com/MicrobiologyETHZ/HoneyScraper.git
```

## Usage
1) Open your terminal.

2) Run your command.
For example:
```
python C:\Users\name\folder\myproject\code\HoneyScraper.py -e my.email@address.com -i 60 -v connected concentration -f myfilename.csv
```
Insert your path to the python script instead.
The following options are available.
```
  -h, --help            show this help message and exit
  -f FILENAME, --filename FILENAME
                        Name of the file where the information is stored. Default: HoneywellValues.csv
  -d DIRECTORY, --directory DIRECTORY
                        Directory in which the file should be saved. Default: location of the script
  -e EMAIL, --email EMAIL
                        An e-mail address, where an e-mail will be sent in case of loss of connection. Mandatory argument.
  -a IPADDRESS, --ipaddress IPADDRESS
                        IP Address of the gas detector. Default: 169.254.60.47
  -i INTERVAL, --interval INTERVAL
                        Time distance between the measurements in seconds. Default: 300
  -v VALUES [VALUES ...], --values VALUES [VALUES ...]
                        Columns to write to the file. Options: ip, connected, state, fault, alarm, concentration, units,
                        temperature, life, flow, low-alarm threshold,high-alarm threshold, time
```

3) You can stop the process using [Ctrl] + [C]

