import tkinter as tk
from tkinter import filedialog
from pyxrk import *
import pyarrow as pa
from pyarrow import csv


# Create a root window and hide it
root = tk.Tk()
root.withdraw()

# Open a file dialog to select the XRK file
file_path = filedialog.askopenfilename(filetypes=[("XRK files", "*.xrk")])
save_path = filedialog.asksaveasfilename(filetypes=[("csv files", "*.csv")])

# Check if a file was selected
if not file_path:
    print("No file selected. Exiting.")


# Load the XRK file using the pyxrk library
run = Run.load(file_path)
# Print some information from the XRK file (you can customize this part)
#print("Racer:", run.racer)
#print("Vehicle:", run.vehicle)
#print("Track:", run.track)
#print("Lap Count:", run.lap_count)
#print("Channel Names:", run.channel_names)
table = run.to_table()

with open(save_path,"wb") as outputfile:
    pa.csv.write_csv(table, save_path)
outputfile.close()
# You can add more analysis code here using the methods provided in the Run class