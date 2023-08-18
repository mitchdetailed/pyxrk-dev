import ctypes
import tkinter as tk
from ctypes import byref
from time import sleep
from tkinter import filedialog
from xrk_parser import XRK, xrkdll
import pyarrow as pa
import pandas as pd
import csv
from tqdm import tqdm

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

ch_names    = ['Time']
ch_units    = ['s']
max_freq    = 0
laptimes    = []
beacons     = []
laps        = 0
logdate     = ''
logtime     = ''
duration    = ''
sample_rate = 100
main_df     = pd.DataFrame(columns=['Time'])

root = tk.Tk()
root.withdraw()
print('Loading Program...')

# Open a file dialog to select the XRK file
file_path = filedialog.askopenfilename(filetypes=[("XRK files", "*.xrk")])
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
        ch_results      = XRK.channel_times_and_samples_by_index(aimlog, channel)
        ch_times        = pa.array(ch_results[0])
        ch_values       = pa.array(ch_results[1])
        ch_table        = pa.Table.from_arrays([ch_times, ch_values], ['Time', channelname])
        ch_df           = ch_table.to_pandas(split_blocks=True, self_destruct=True)
        del ch_table
        ch_df.columns   = ['Time', channelname]
        ch_df['Time']   = pd.to_timedelta(ch_df['Time'], unit='s')
        ch_df.set_index('Time', inplace=True)
        hz              = hz_to_pandas_freq(sample_rate)
        ch_df           = ch_df.resample(hz).ffill()
        main_df         = pd.merge(main_df, ch_df, on='Time', how='outer')
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
        hz              = hz_to_pandas_freq(sample_rate)
        ch_df           = ch_df.resample(hz).ffill()
        main_df         = pd.merge(main_df, ch_df, on='Time', how='outer')
        ch_names.append(channelname)
        ch_units.append(channelunit)

print('\r\nSorting...')
main_df.sort_values(by='Time', inplace=True)
main_df.set_index('Time', inplace=True, drop=False)
main_df = main_df.resample(hz).ffill()
main_df['Time'] = main_df['Time'].dt.total_seconds()
main_df = main_df.fillna(0)
outputfile = file_path[:-4]+'.csv'
print('\r\nWriting to CSV...\r\n Please wait patiently...')
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
        ['Sample Rate',sample_rate,'Hz','','End Time',duration,'s'],
        ['Duration',duration,'s','','Start Distance'],
        ['Range','entire outing','','','End Distance'],
        ['Beacon Markers',beacons_str],
        [],
        [],
        ch_names,
        ch_units
        ]
    writer.writerows(header)

main_df.to_csv(outputfile, index=False, mode='a', quoting=csv.QUOTE_ALL)

XRK.close(aimlog)