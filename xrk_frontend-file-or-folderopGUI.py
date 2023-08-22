import ctypes
from tkinter import filedialog, messagebox
import tkinter as tk
from ctypes import byref
from time import sleep 
import time
from xrk_parser import XRK, xrkdll
import pyarrow as pa
import pandas as pd
import csv
from tqdm import tqdm
import os
import sys

def resource(relative_path):
    base_path = getattr(
        sys,
        '_MEIPASS',
        os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

iconbmp = resource("XRK-2-CSV.ico")
# Determine if the application is running as a script or as a packaged executable


request_folder  = 0
request_file    = 0
print("Loading Program...")
def filefunc():
    global request_file
    request_file = 1
    root.destroy()

def folderfunc():
    global request_folder
    request_folder = 1
    root.destroy()


def load_xrk_file():
    # Prompt the user to select an .xrk file
    file_path = filedialog.askopenfilename(filetypes=[("XRK files", "*.xrk")])
    
    if not file_path:
        return
    
    # Get the directory and the filename without extension
    directory, filename = os.path.split(file_path)
    basename = os.path.splitext(filename)[0]
    
    # Check if a matching .csv file exists in the directory
    csv_file_path = os.path.join(directory, basename + ".csv")
    
    if os.path.exists(csv_file_path):
        messagebox.showinfo("Result", ".xrk file has matching .csv file")

    else:
        unmatched_file_paths.append(file_path)


def check_files_in_directory(directory):
    """Check for .xrk files where no corresponding .csv exists."""
    global unmatched_file_paths  # Refer to the global list
    xrk_files = [file for file in os.listdir(directory) if file.endswith(".xrk")]
    csv_files = [file for file in os.listdir(directory) if file.endswith(".csv")]

    for xrk_file in xrk_files:
        # Check if the .xrk file has a corresponding .csv file
        csv_file = xrk_file.replace(".xrk", ".csv")
        if csv_file not in csv_files:
            full_path = os.path.join(directory, xrk_file)
            unmatched_file_paths.append(full_path)

    if unmatched_file_paths:
        files_list = "\n".join(unmatched_file_paths)
        #messagebox.showinfo("Result", f".xrk files without matching .csv files:\n\n{files_list}")
    else:
        messagebox.showinfo("Result", "All .xrk files have matching .csv files or no .xrk files found.")


def select_folder():
    """Let the user select a folder and check it."""
    folder_path = filedialog.askdirectory()
    if folder_path:
        check_files_in_directory(folder_path)

def hz_to_pandas_freq(hz):
    """
    Convert a frequency in Hz to a pandas time frequency string.
    Parameters:
    - hz (float): Frequency in Hz.
    Returns:
    - str: Corresponding pandas time frequency string.
    """
    # Calculate the time period in seconds
    period_seconds = 1 / hz

    # Convert the period to the appropriate pandas time frequency string
    if period_seconds >= 1:
        return f"{int(period_seconds)}S"
    elif period_seconds >= 1e-3:
        return f"{int(period_seconds * 1e3)}L"
    elif period_seconds >= 1e-6:
        return f"{int(period_seconds * 1e6)}U"
    else:
        return f"{int(period_seconds * 1e9)}N"


# Create the main window
root = tk.Tk()


root.iconbitmap(iconbmp)
root.title("Choose an Option")
root.geometry("450x230")

# Center the window on the screen
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates to center the window
sizex = (screen_width / 2) - (450 / 2)
sizey = (screen_height / 2) - (230 / 2)

root.geometry(f"+{int(sizex)}+{int(sizey)}")

# Create the buttons with custom width and height
btn1 = tk.Button(root, text="Single\nXRK\nFile", command=filefunc, width=10, height=5, font=("Arial", 20, "bold"), foreground="black", background="green")
btn2 = tk.Button(root, text="Entire\nXRK\nFolder", command=folderfunc, width=10, height=5, font=("Arial", 20, "bold"), foreground="black", background="yellow")

# Place the buttons side by side using grid
btn1.grid(row=0, column=0, padx=20, pady=20)
btn2.grid(row=0, column=1, padx=20, pady=20)

root.mainloop()
# Global list to store full path names of unmatched .xrk files
unmatched_file_paths = []

if request_folder == 1:
    select_folder()

elif request_file == 1:
    load_xrk_file()

starttime = time.time()
for file_path in unmatched_file_paths:
    ch_names    = ['Time']
    ch_units    = ['s']
    max_freq    = 0
    laptimes    = []
    beacons     = []
    laps        = 0
    logdate     = ''
    logtime     = ''
    duration    = ''
    gps_sample_rate = 100
    max_sample_rate = gps_sample_rate

    main_df     = df = pd.DataFrame({'placeholder': [0] }, index=[pd.Timedelta(seconds=0)])
    print('Converting %s' % (file_path))

    aimlog = XRK(file_path)
    track       = XRK.track_name(aimlog)
    vehicle     = XRK.vehicle_name(aimlog)
    driver      = XRK.racer_name(aimlog)
    comment     = XRK.championship_name(aimlog)
    session     = XRK.session_type(aimlog)
    logdate     = XRK.log_date(aimlog)
    logtime     = XRK.log_time(aimlog)
    laps        = XRK.lap_count(aimlog)
    laptimes    = XRK.lap_times(aimlog)
    beacons     = XRK.lap_beacons(aimlog)
    if len(beacons) > 1 and beacons[0] == 0.0:
        beacons = beacons[1:]
    beacons_str = " ".join([str(f) for f in beacons])
    duration    = int(round((beacons[-1] + laptimes[-1]), 0))
    total_ch    = (int(XRK.channel_count(aimlog)) + int(XRK.GPS_channel_count(aimlog)))
    ch_count = XRK.channel_count(aimlog)
    print('\r\nAnalyzing Non GPS Channels...')
    for channel in tqdm(range(ch_count), ascii=True, unit='ch'):
        samplecount     = XRK.channel_sample_count_by_index(aimlog, channel)
        if samplecount > 0:
            channelname     = XRK.channel_name_by_index(aimlog, channel)
            channelunit     = XRK.channel_units_by_index(aimlog, channel)
            channelhz       = XRK.channel_frequency_by_index(aimlog, channel)
            if channelhz > max_sample_rate:
                max_sample_rate = channelhz
            ch_results      = XRK.channel_times_and_samples_by_index(aimlog, channel)
            ch_times        = pa.array(ch_results[0], type=pa.float32())
            ch_values       = pa.array(ch_results[1], type=pa.float32())
            ch_table        = pa.Table.from_arrays([ch_times, ch_values], ['Time', channelname])
            ch_df           = ch_table.to_pandas(split_blocks=True, self_destruct=True)
            del ch_table
            ch_df.columns   = ['Time', channelname]
            ch_df['Time']   = pd.to_timedelta(ch_df['Time'], unit='s')
            ch_df.set_index('Time', inplace=True)
            hz              = hz_to_pandas_freq(channelhz)
            new_index = pd.timedelta_range(start='0s', end=ch_df.index[-1], freq=hz)
            ch_df = ch_df.reindex(new_index, method='ffill')
            main_df         = main_df.merge(ch_df, left_index=True, right_index=True, how='outer')
            ch_names.append(channelname)
            ch_units.append(channelunit)

    gps_ch_count = XRK.GPS_channel_count(aimlog)
    print('\r\nAnalyzing GPS Channels...')
    for channel in tqdm(range(gps_ch_count), ascii=True, unit='ch'):
        samplecount     = XRK.GPS_channel_sample_count_by_index(aimlog, channel)
        if samplecount > 0:
            channelname     = XRK.GPS_channel_name_by_index(aimlog, channel)
            channelunit     = XRK.GPS_channel_units_by_index(aimlog, channel)
            channelhz       = XRK.GPS_channel_frequency_by_index(aimlog, channel)
            ch_results      = XRK.GPS_channel_times_and_samples_by_index(aimlog, channel)
            ch_times        = pa.array(ch_results[0], type=pa.float32()) # original values are float64
            ch_values       = pa.array(ch_results[1], type=pa.float32()) # original values are float64
            ch_table        = pa.Table.from_arrays([ch_times, ch_values], ['Time', channelname])
            ch_df           = ch_table.to_pandas(split_blocks=True, self_destruct=True)
            del ch_table
            ch_df.columns   = ['Time', channelname]
            ch_df['Time']   = ch_df['Time'] / 1000
            ch_df['Time']   = pd.to_timedelta(ch_df['Time'], unit='s')
            ch_df.set_index('Time', inplace=True)
            hz              = hz_to_pandas_freq(gps_sample_rate)
            new_index = pd.timedelta_range(start='0s', end=ch_df.index[-1], freq=hz)
            ch_df = ch_df.reindex(new_index, method='ffill')
            main_df         = main_df.merge(ch_df, left_index=True, right_index=True, how='outer')
            ch_names.append(channelname)
            ch_units.append(channelunit)

    print('\r\nSorting...')
    ch_units = ['' if item == "#" else item for item in ch_units]
    main_df.drop(columns=['placeholder'], inplace=True)
    main_df.reset_index()
    main_df['Time'] = main_df.index.total_seconds()
    cols = ['Time'] + [col for col in main_df if col != 'Time']
    main_df = main_df[cols]
    main_df = main_df.ffill().fillna(0)
    #main_df['Time'] = main_df['Time'].round(3)
    outputfile = file_path[:-4]+'.csv'
    print('\r\nWriting to CSV...\r\nPlease wait patiently...')
    with open(outputfile, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile,quoting=csv.QUOTE_ALL)
        header = [
            ['Format', 'MoTeC CSV File','','','Workbook'],
            ['Venue',track,'','','Worksheet'],
            ['Vehicle',vehicle,'','','Vehicle Desc'],
            ['Driver',driver,'','','Engine ID'],
            ['Device','AiM Ported'],
            ['Comment',comment,'','','Session',session],
            ['Log Date',logdate,'','','Origin Time','0','s'],
            ['Log Time',logtime,'','','Start Time','0','s'],
            ['Sample Rate',max_sample_rate,'Hz','','End Time',duration,'s'],
            ['Duration',duration,'s','','Start Distance'],
            ['Range','entire outing','','','End Distance'],
            ['Beacon Markers',beacons_str],
            [],
            [],
            ch_names,
            ch_units,
            [],
            []
            ]
        
        writer.writerows(header)

    main_df.to_csv(outputfile, index=False, header=False, mode='a', quoting=csv.QUOTE_ALL)
    XRK.close(aimlog)
    print('Conversion Completed for %s\n' % file_path)

end_time = time.time()
elapsed_time = end_time-starttime
print("total time elapsed : %2.1f seconds\n Closing program..." % (elapsed_time))
sleep(1)
