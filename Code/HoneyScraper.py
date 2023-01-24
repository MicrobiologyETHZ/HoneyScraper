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
IPAdress = '169.254.60.47'
interval = 10 #seconds
# TODO: add time with time zone. There is an incompatibility with the package time and pytz or datetime?
switzerland = timezone('Europe/Zurich')
sui_time = datetime.now(switzerland)

# create path from variables
path = os.path.join(directory, filename)

# https://pypi.org/project/midas/
# function to get the dictionary
async def get():
    async with GasDetector(IPAdress) as detector:
        print(await detector.get())
        return await detector.get()

# starts the event loop and runs the coroutine
mydictionary = asyncio.run(get())
# just print the value of fault not a dictionary
mydictionary["fault"] = mydictionary["fault"]["status"]
# add current time to dictionary
mydictionary["time"] = sui_time.strftime('%Y-%m-%d_%H-%M-%S')

print(mydictionary)

# if the file does not exist, save the dictionary as a csv dataframe
if not os.path.isfile(path):
    # save it as a pandas dataframe
    #df = pd.DataFrame.from_dict(dictionary)
    df = pd.DataFrame([mydictionary])
    # write
    df.to_csv(filename, index=False)


# call this part of code every x minutes

# flush --> write it to the file (.csv)
## if file does exist --> add new line
async def write_information(mydictionary, path):
    row = mydictionary.values()
    # open the existing csv file in append mode
    # Create a file object for this file
    with open(path, "a", newline='') as myobject:
        # pass this object to writer and get a writer object
        writer_object = writer(myobject)

        # write the row
        writer_object.writerow(row)

        #close the filename
        myobject.close()

orig_start_time = time.time()

# call write_information all x seconds
async def call_function(mydictionary, path, interval, periodic_function):
    while True:
        # prints time since beginning when it is running
        print(round(time.time() - orig_start_time, 1), "Writing information to csv file...")

        await asyncio.gather(
            asyncio.sleep(interval),
            periodic_function(mydictionary, path),
        )


asyncio.run(call_function(mydictionary, path, interval, write_information))
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




