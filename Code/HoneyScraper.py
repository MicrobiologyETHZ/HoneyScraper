# import packages
import asyncio
import time
from midas import GasDetector
import os.path
import argparse
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from pytz import timezone


# function to get the dictionary
# https://pypi.org/project/midas/
# https://github.com/numat/midas

async def get_new_data():
    # "with" --> we are using a context manager --> prevents a lot of boiler plate code
    async with GasDetector(IPAddress) as detector:
        #print(await detector.get_new_data())
        # return current state
        return await detector.get()


# call this part of code every x minutes
# flush --> write it to the file (.csv)
async def write_dict_to_csv(path, values_to_write, error):
    sui_time = datetime.now(switzerland)
    if type(error)==list:
        # we need this because async.gather returns a list of values (one for each function)
        error=error[1]

    try:
        # update the dictionary
        # call function directly, since the event loop was already called
        dictionary = await get_new_data()
        # just print the value of fault not a dictionary
        dictionary["fault"] = dictionary["fault"]["status"]
        # add current time to dictionary

        dictionary["time"] = sui_time.strftime('%Y-%m-%d_%H-%M-%S')
        # values will be always in the same order
        # try/except clause to catch potential KeyError
        try:
            row = [dictionary[key] for key in values_to_write]
        except:
            print("An unexpected key was provided in the dictionary")

    # in case of connection loss
    except:
        # error counter for exception --> only do e-mail for the first exception
        error = error + 1
        #print(error)
        row=['NA']*len(values_to_write)
        if error == 1:
            print("Connection was lost: e-mail is being sent.")

    # happens anyways
    finally:
        # needed to join the values
        row = [str(r) if type(r) != str else r for r in row]
        #print(row)

        # write the row with the new values
        with open(path, "a", newline='') as obj:
            obj.write(",".join(row) + "\n")
        print(sui_time.strftime('%Y-%m-%d_%H-%M-%S'))
    return error


# call write_dict_to_csv all x seconds
async def call_function(values_to_write, path, interval, periodic_function, error):

    while True:
        # prints time since beginning when it is running
        print("Writing information to csv file...")

        # asyncio.gather() allows the caller to group multiple awaitables together
        # once grouped the awaitables can be executed concurrently, awaited and cancelled
        # it also prevents drift in the intervals (drift = when time doesn't match a reference time, very common
        # in computationally intensive processes)
        # very small drifts can still happen
        error = await asyncio.gather(
            asyncio.sleep(interval),
            periodic_function(path, values_to_write, error),
        )

if __name__ == '__main__':
    # the values that can be specified by the user
    parser = argparse.ArgumentParser(prog='HoneyScraper',
                                     description="Get information from the Honeywell Midas Gas Detector")
    parser.add_argument("-f", "--filename", default="HoneywellValues.csv",
                        help="Name of the file where the information is stored. Example: values.csv")
    parser.add_argument("-d", "--directory", default=os.path.dirname(os.path.realpath(__file__)),
                        help="Directory in which the file should be saved. Default: location of the script")
    parser.add_argument("-a", "--ipaddress", type=str, default='169.254.60.47',
                        help="IP Address of the gas detector. Default: 169.254.60.47")
    parser.add_argument("-i", "--interval", type=float, default=300,
                        help="Time distance between the measurements in seconds. Default: 300")
    parser.add_argument("-v", "--values", nargs='+',
                        default=('ip', 'connected', 'state', 'fault', 'alarm', 'concentration', 'units', 'temperature',
                                 'life', 'flow', 'low-alarm threshold', 'high-alarm threshold', 'time'),
                        help="Columns to write to the file. Options: ip, connected, state, fault, "
                             "alarm, concentration, units, temperature, life, flow, low-alarm threshold,"
                             "high-alarm threshold, time")
    # run the parser and place the extracted data in an argparse.Namespace object
    args = parser.parse_args()

    # variables
    filename = args.filename
    directory = args.directory # "C:/Users/lilit/Git_repos/HoneyScraper/Code/"
    # create path from variables
    print(str("Saving " + filename + " to " + directory))
    path = os.path.join(directory, filename)
    IPAddress = args.ipaddress
    #IPAddress='169.254.60.47'
    interval = args.interval  # seconds
    switzerland = timezone('Europe/Zurich')
    # order of the columns and which columns we want
    values_to_write = args.values
    # how many times the error occurred
    error = 0

    # write the title
    with open(path, "a", newline='') as obj:
        obj.write(",".join(values_to_write) + "\n")

    # starts the event loop and runs the coroutine (coroutines allow multitasking)
    try:
        valuedictionary = asyncio.run(get_new_data())
        # just print the value of fault not a dictionary
        valuedictionary["fault"] = valuedictionary["fault"]["status"]
        # add current time to dictionary
        sui_time = datetime.now(switzerland)
        valuedictionary["time"] = sui_time.strftime('%Y-%m-%d_%H-%M-%S')

    except:
        row=['NA']*len(values_to_write)
        row = [str(r) if type(r) != str else r for r in row]
        print(row)
        with open(path, "a", newline='') as obj:
            obj.write(",".join(row) + "\n")

    # needed to print the run time in the console
    orig_start_time = time.time()

    # start the process
    asyncio.run(call_function(values_to_write, path, interval, write_dict_to_csv, error))



# warning e mail if it's not running or if the output is only zeroes




