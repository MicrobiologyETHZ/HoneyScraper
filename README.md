# HoneyScraper
Python Script that accesses the Honeywell Midas Gas Detector periodically and writes the information to a csv file.

## Installation
```
git clone https://github.com/MicrobiologyETHZ/HoneyScraper.git
```

## Usage
1) Open your terminal.
2) Write the following command, but insert the name of your environment instead.
```
conda activate {environment name}
```
In case you don't remember the name of your environment, you can see all the environments using 
```
conda env list
```
In case you don't have pw.txt. Contact Lilith Feer or uncomment all the lines that affect the e-mail sending. (line 65-77, 118-120, 150-155 and remove the function inputs (honeywellmailaddress, apppassword and emailaddress))

3) Run your command.
For example:
```
python C:\Users\name\folder\myproject\code\HoneyScraper.py -i 60 -v connected concentration -f myfilename.csv
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

4) You can stop the process using [Ctrl] + [C]

