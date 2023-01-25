# import packages
import asyncio
import time
from midas import GasDetector
import pandas as pd
import os.path
from csv import writer
from datetime import datetime
from pytz import timezone


# variables
filename = "HoneyWellValues.csv"
directory = "C:/Users/lilit/Git_repos/HoneyScraper/Code/"
# create path from variables
path = os.path.join(directory, filename)
IPAdress = '169.254.60.47'
interval = 10 #seconds
switzerland = timezone('Europe/Zurich')
sui_time = datetime.now(switzerland)


# function to get the dictionary
# https://pypi.org/project/midas/
# https://github.com/numat/midas
async def get():
    # "with" --> we are using a context manager --> prevents a lot of boiler plate code
    async with GasDetector(IPAdress) as detector:
        print(await detector.get())
        # return current state
        return await detector.get()

# starts the event loop and runs the coroutine (coroutines allow multitasking)
valuedictionary = asyncio.run(get())
# just print the value of fault not a dictionary
valuedictionary["fault"] = valuedictionary["fault"]["status"]
# add current time to dictionary
valuedictionary["time"] = sui_time.strftime('%Y-%m-%d_%H-%M-%S')

# if the file does not exist, save the dictionary as a csv dataframe
if not os.path.isfile(path):
    # save it as a pandas dataframe
    df = pd.DataFrame([valuedictionary])
    # write
    df.to_csv(filename, index=False)

# call this part of code every x minutes
# flush --> write it to the file (.csv)
async def write_information(dictionary, path):
    row = dictionary.values()
    # open the existing csv file in append mode
    # newline = '' prevents that there are empty lines in between the newly written rows
    with open(path, "a", newline='') as obj:
        # pass this object to writer (converts data into a delimited string) and get a writer object
        writer_object = writer(obj)

        # write the row
        writer_object.writerow(row)

        #close the object
        obj.close()

orig_start_time = time.time()

# call write_information all x seconds
async def call_function(dictionary, path, interval, periodic_function):
    while True:
        # prints time since beginning when it is running
        print(round(time.time() - orig_start_time, 1), "Writing information to csv file...")

        # asyncio.gather() allows the caller to group multiple awaitables together
        # once grouped the awaitables can be executed concurrently, awaited and cancelled
        # it also prevents drift in the intervals (drift = when time doesn't match a reference time, very common
        # in computationally intensive processes)
        # very small drifts can still happen
        await asyncio.gather(
            asyncio.sleep(interval),
            periodic_function(dictionary, path),
        )


asyncio.run(call_function(valuedictionary, path, interval, write_information))

#def stop():
#    task.cancel()

#loop = asyncio.get_event_loop()
#loop.call_later(interval, stop)
#task = loop.create_task(write_information(dictionary, path, interval))

# if it is still running, cancel
#try:
#    loop.run_until_complete(task)
#except asyncio.CancelledError:
#    pass






# warning e mail if it's not running or if the output is only zeroes




