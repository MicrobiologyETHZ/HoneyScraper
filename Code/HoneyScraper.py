# import packages
import asyncio
import time
from midas import GasDetector
import pandas as pd
import os.path
from csv import writer
from datetime import datetime
from pytz import timezone


# function to get the dictionary
# https://pypi.org/project/midas/
# https://github.com/numat/midas

async def get():
    # todo rename the function to be more specific (ex. get_detector_data)
    # "with" --> we are using a context manager --> prevents a lot of boiler plate code
    async with GasDetector(IPAdress) as detector:
        print(await detector.get())
        # return current state
        return await detector.get()


# call this part of code every x minutes
# flush --> write it to the file (.csv)
# todo rename function to be more specific (ex. write_detection_dict_to_csv)
async def write_information(dictionary, path,
                            values_to_write = ('ip', 'connected', 'state', 'fault', 'alarm', 'concentration',
                                               'units', 'temperature', 'life', 'flow', 'low-alarm threshold',
                                               'high-alarm threshold', 'time')):
    # this is potentially problematic, not sure the values will be always in the same order
    # We won't know if something has gone wrong, it will just keep writing all the values
    row = dictionary.values()
    # todo replace the line above with the following:
    # row = [dictionary[key] for key in values_to_write]
    # you can also add try/except clause to catch potential KeyError

    # open the existing csv file in append mode
    # newline = '' prevents that there are empty lines in between the newly written rows

    # todo simplify the code below
    # not sure why you are using such complicated code, with context manager you do not need to closes the file for you
    # also you do not need csv module for this task
    # can be replaced with this:

    #with open(path, "a") as obj:
    #   obj.write(",".join(row))

    with open(path, "a", newline='') as obj:
        # pass this object to writer (converts data into a delimited string) and get a writer object
        writer_object = writer(obj)

        # write the row
        writer_object.writerow(row)

        #close the object
        obj.close()


# call write_information all x seconds
async def call_function(dictionary, path, interval, periodic_function):
    # todo this is your main function, it should be repeated calling get() -> otherwise how is dictionary updated?
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
            # todo call get() function to get the new dictionary values i.e. lines 94 to 98

            periodic_function(dictionary, path),
        )

if __name__ == '__main__':
    # todo look into argparse module -> these arguments should be specified by the user, with values below set as defaults
    # variables
    filename = "HoneyWellValues.csv"
    directory = "C:/Users/lilit/Git_repos/HoneyScraper/Code/"
    # create path from variables
    path = os.path.join(directory, filename)
    IPAdress = '169.254.60.47'
    interval = 10  # seconds
    switzerland = timezone('Europe/Zurich')
    sui_time = datetime.now(switzerland)

    # todo this logic should be inside your main function not here
    # starts the event loop and runs the coroutine (coroutines allow multitasking)
    valuedictionary = asyncio.run(get())
    # just print the value of fault not a dictionary
    valuedictionary["fault"] = valuedictionary["fault"]["status"]
    # add current time to dictionary
    valuedictionary["time"] = sui_time.strftime('%Y-%m-%d_%H-%M-%S')

    # if the file does not exist, save the dictionary as a csv dataframe

    # todo won't need this part once this is inside the main function
    if not os.path.isfile(path):
        # save it as a pandas dataframe
        df = pd.DataFrame([valuedictionary])
        # write
        df.to_csv(filename, index=False)

    orig_start_time = time.time()


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




