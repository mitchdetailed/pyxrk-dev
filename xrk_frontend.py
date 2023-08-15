import ctypes
import tkinter as tk
from ctypes import byref
from time import sleep
from tkinter import filedialog

from xrk_parser import XRK, xrkdll

root = tk.Tk()
root.withdraw()

# Open a file dialog to select the XRK file
file_path = filedialog.askopenfilename(filetypes=[("XRK files", "*.xrk")])

aimlog = XRK(file_path)
print('%s' %(XRK.track_name(aimlog)))
print('%s' %(XRK.vehicle_name(aimlog)))
print('%s' %(XRK.venue_type(aimlog)))
print('%s' %(XRK.racer_name(aimlog)))
print('%s' %(XRK.log_datetime(aimlog)))
print('%s' %(XRK.championship_name(aimlog)))

x = XRK.lap_count(aimlog)
print(x)
x = XRK.lap_times(aimlog)
print(x)
x = XRK.lap_beacons(aimlog)
print(x)
sleep(3)
x = XRK.channel_name_by_index(aimlog,0)
print(x)
x = XRK.channel_times_and_samples_by_index(aimlog,0)
items = XRK.channel_count(aimlog)

x = XRK.channel_frequency(aimlog,'ECU_ERR_ECT')
print(x)
sleep(10)

for i in range(items):
    x=XRK.channel_name_by_index(aimlog,i)
    print(x)
    x = XRK.channel_frequency_by_index(aimlog,i)
    print(x)
## TO DO 
    # get channel frequency function written. 
    # find a way to dump to csv using pandas df.









XRK.close(aimlog)


#def round_to_closest(val, numbers):
#    """
#    Round the value to the closest number in the provided list.
#    """
#    return min(numbers, key=lambda x: abs(x - val))

# List of numbers
#numbers = [1, 2, 5, 10, 20, 25, 50, 100, 200, 500, 1000]

# Test the function with a sample value
#sample_value = 37
#rounded_value = round_to_closest(sample_value, numbers)

#rounded_value
