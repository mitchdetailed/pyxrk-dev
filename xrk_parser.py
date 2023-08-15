import ctypes
from ctypes import byref
import tkinter as tk
from tkinter import filedialog
from time import sleep

# Load the DLL
xrkdll = ctypes.WinDLL('MatLabXRK-2017-64-ReleaseU.dll')

# Begin DLL function prototypes

# idxf = index of file
# idxl = index of lap
# idxc = index of channel

# int open_file(char const* full_path_name)
xrkdll.open_file.restype = ctypes.c_int
xrkdll.open_file.argtypes = [ctypes.c_char_p]

# int close_file_n(char const* full_path_name)
xrkdll.close_file_n.restype = ctypes.c_int
xrkdll.close_file_n.argtypes = [ctypes.c_char_p]

# int close_file_i(int idx)
xrkdll.close_file_i.restype = ctypes.c_int
xrkdll.close_file_i.argtypes = [ctypes.c_int]

# int get_vehicle_name(int idx)
xrkdll.get_vehicle_name.restype = ctypes.c_char_p
xrkdll.get_vehicle_name.argtypes = [ctypes.c_int]

# int get_track_name(int idx)
xrkdll.get_track_name.restype = ctypes.c_char_p
xrkdll.get_track_name.argtypes = [ctypes.c_int]

# int get_racer_name(int idx)
xrkdll.get_racer_name.restype = ctypes.c_char_p
xrkdll.get_racer_name.argtypes = [ctypes.c_int]

# int get_championship_name(int idx)
xrkdll.get_championship_name.restype = ctypes.c_char_p
xrkdll.get_championship_name.argtypes = [ctypes.c_int]

# int get_venue_type_name(int idx)
xrkdll.get_venue_type_name.restype = ctypes.c_char_p
xrkdll.get_venue_type_name.argtypes = [ctypes.c_int]

# int getdate_and_time(int idx)

class dts(ctypes.Structure):
    _fields_ = [("second", ctypes.c_int),("minute", ctypes.c_int),("hour", ctypes.c_int),("day", ctypes.c_int),("month", ctypes.c_int),("year", ctypes.c_int)]
    
xrkdll.get_date_and_time.restype = ctypes.POINTER(dts)
xrkdll.get_date_and_time.argtypes = [ctypes.c_int]

# int get_laps_count(int idx)
xrkdll.get_laps_count.restype = ctypes.c_int
xrkdll.get_laps_count.argtypes = [ctypes.c_int]

# int get_lap_info(int idxf, int idxl, double* pstart, double* pduration)
xrkdll.get_lap_info.restype = ctypes.c_int
xrkdll.get_lap_info.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)]

# int get_channels_count(int idx)
xrkdll.get_channels_count.restype = ctypes.c_int
xrkdll.get_channels_count.argtypes = [ctypes.c_int]

# in get_channel_name(int idxf, int idxc)
xrkdll.get_channel_name.restype = ctypes.c_char_p
xrkdll.get_channel_name.argtypes = [ctypes.c_int, ctypes.c_int]

# in get_channel_units(int idxf, int idxc)
xrkdll.get_channel_units.restype = ctypes.c_char_p
xrkdll.get_channel_units.argtypes = [ctypes.c_int, ctypes.c_int]

# int get_channel_samples_count(int idxf, int idxc)
xrkdll.get_channel_samples_count.restype = ctypes.c_int
xrkdll.get_channel_samples_count.argtypes = [ctypes.c_int, ctypes.c_int]

# int get_channel_samples(int idxf, int idxc, double* ptimes, double* pvalues, int cnt)
xrkdll.get_channel_samples.restype = ctypes.c_int
xrkdll.get_channel_samples.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]

# int get_lap_channel_samples_count(int idxf, int idxl, int idxc)
xrkdll.get_lap_channel_samples_count.restype = ctypes.c_int
xrkdll.get_lap_channel_samples_count.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]

# int get_lap_channel_samples(int idxf, int idxl, int idxc, double* ptimes, double* pvalues, int cnt)
xrkdll.get_lap_channel_samples.restype = ctypes.c_int
xrkdll.get_lap_channel_samples.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]

# int get_GPS_channels_count(int idx)
xrkdll.get_GPS_channels_count.restype = ctypes.c_int
xrkdll.get_GPS_channels_count.argtypes = [ctypes.c_int]

# in get_GPS_channel_name(int idxf, int idxc)
xrkdll.get_GPS_channel_name.restype = ctypes.c_char_p
xrkdll.get_GPS_channel_name.argtypes = [ctypes.c_int, ctypes.c_int]

# in get_GPS_channel_units(int idxf, int idxc)
xrkdll.get_GPS_channel_units.restype = ctypes.c_char_p
xrkdll.get_GPS_channel_units.argtypes = [ctypes.c_int, ctypes.c_int]

# int get_GPS_channel_samples_count(int idxf, int idxc)
xrkdll.get_GPS_channel_samples_count.restype = ctypes.c_int
xrkdll.get_GPS_channel_samples_count.argtypes = [ctypes.c_int, ctypes.c_int]

# int get_GPS_channel_samples(int idxf, int idxc, double* ptimes, double* pvalues, int cnt)
xrkdll.get_GPS_channel_samples.restype = ctypes.c_int
xrkdll.get_GPS_channel_samples.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]

# int get_lap_GPS_channel_samples_count(int idxf, int idxl, int idxc)
xrkdll.get_lap_GPS_channel_samples_count.restype = ctypes.c_int
xrkdll.get_lap_GPS_channel_samples_count.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]

# int get_lap_GPS_channel_samples(int idxf, int idxl, int idxc, double* ptimes, double* pvalues, int cnt)
xrkdll.get_lap_GPS_channel_samples.restype = ctypes.c_int
xrkdll.get_lap_GPS_channel_samples.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]

# int get_GPS_raw_channels_count(int idx)
xrkdll.get_GPS_raw_channels_count.restype = ctypes.c_int
xrkdll.get_GPS_raw_channels_count.argtypes = [ctypes.c_int]

# int get_GPS_raw_channel_name(int idxf, int idxc)
xrkdll.get_GPS_raw_channel_name.restype = ctypes.c_char_p
xrkdll.get_GPS_raw_channel_name.argtypes = [ctypes.c_int, ctypes.c_int]

# int get_GPS_raw_channel_units(int idxf, int idxc)
xrkdll.get_GPS_raw_channel_units.restype = ctypes.c_char_p
xrkdll.get_GPS_raw_channel_units.argtypes = [ctypes.c_int, ctypes.c_int]

# int get_GPS_raw_channel_samples_count(int idxf, int idxc)
xrkdll.get_GPS_raw_channel_samples_count.restype = ctypes.c_int
xrkdll.get_GPS_raw_channel_samples_count.argtypes = [ctypes.c_int, ctypes.c_int]

# int get_GPS_raw_channel_samples(int idxf, int idxc, double* ptimes, double* pvalues, int cnt)
xrkdll.get_GPS_raw_channel_samples.restype = ctypes.c_int
xrkdll.get_GPS_raw_channel_samples.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]

# int get_lap_GPS_raw_channel_samples_count(int idxf, int idxl, int idxc)
xrkdll.get_lap_GPS_raw_channel_samples_count.restype = ctypes.c_int
xrkdll.get_lap_GPS_raw_channel_samples_count.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]

# int get_lap_GPS_raw_channel_samples(int idxf, int idxl, int idxc, double* ptimes, double* pvalues, int cnt)
xrkdll.get_lap_GPS_raw_channel_samples.restype = ctypes.c_int
xrkdll.get_lap_GPS_raw_channel_samples.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]

## END DLL Function Prototypes

class XRK():
    def __init__(self, filename):      
        self.filename = filename
        self.filepointer = ctypes.c_char_p(self.filename.encode())
        self.idxf = xrkdll.open_file(self.filepointer)
        self.channels = self.channel_list()
        self.GPS_channels = self.GPS_channel_list()
        self.GPS_raw_channels = self.GPS_raw_channel_list()
        if not self.idxf > 0:
            del self 
           
    def close(self):
        success = xrkdll.close_file_i(self.idxf)
        return (success > 0)
    
    # returns a string of the vehicle name
    def vehicle_name(self):
        return xrkdll.get_vehicle_name(self.idxf).decode('utf-8')
    
    # returns a string of the track name   
    def track_name(self):
        return xrkdll.get_track_name(self.idxf).decode('utf-8')
    
    # returns a string of the racer's name
    def racer_name(self):
        return xrkdll.get_racer_name(self.idxf).decode('utf-8')
    
    # returns a string of the championship name
    def championship_name(self):
        return xrkdll.get_championship_name(self.idxf).decode('utf-8')
    
    # returns a string of the venue type
    def venue_type(self):
        return xrkdll.get_venue_type_name(self.idxf).decode('utf-8')
    
    def log_datetime(self):
        logsec = xrkdll.get_date_and_time(self.idxf).contents.second
        logmin = xrkdll.get_date_and_time(self.idxf).contents.minute
        loghour = xrkdll.get_date_and_time(self.idxf).contents.hour
        logday = xrkdll.get_date_and_time(self.idxf).contents.day
        logmonth = (xrkdll.get_date_and_time(self.idxf).contents.month)+1
        logyear = (xrkdll.get_date_and_time(self.idxf).contents.year)+1900
        return f'{logmonth:02}-{logday:02}-{logyear:04} {loghour:02}:{logmin:02}:{logsec:02}'

    # returns an integer lap count
    def lap_count(self):
        return xrkdll.get_laps_count(self.idxf)
    
    # returns a list of the lap times in the given run
    def lap_times(self):
        laps = self.lap_count()
        current_start = ctypes.c_double(0)
        current_duration = ctypes.c_double(0)
        lap_times = []
        for i in range(laps):
            xrkdll.get_lap_info(self.idxf, i, byref(current_start), byref(current_duration))
            lap_times.append(round(current_duration.value,3))
        return lap_times
        
    def lap_beacons(self):
        laps = self.lap_count()
        current_start = ctypes.c_double(0)
        current_duration = ctypes.c_double(0)
        lap_starts = []
        for i in range(laps):
            xrkdll.get_lap_info(self.idxf, i, byref(current_start), byref(current_duration))
            lap_starts.append(round(current_start.value,3))
        return lap_starts
        
    ############################################################################
    ## REGULAR DATA CHANNEL MEHTODS
    ############################################################################
        
    def channel_count(self):
        return xrkdll.get_channels_count(self.idxf)
             
    def channel_list(self):
        channel_names = []
        for i in range(self.channel_count()):
            channel_i = xrkdll.get_channel_name(self.idxf, i).decode('utf-8')
            channel_names.append(channel_i) 
        return channel_names
    
    def channel_name_by_index(self, idxc):
        return xrkdll.get_channel_name(self.idxf, idxc).decode('utf-8')
        
    def channel_sample_count(self, channel_name):
        try:
            idxc = self.channels.index(channel_name)
            return xrkdll.get_channel_samples_count(self.idxf, idxc)
        except:
            return 0

    def channel_sample_count_by_index(self, idxc):
        return xrkdll.get_channel_samples_count(self.idxf, idxc)
    
    def channel_units(self, channel_name):
        try:
            idxc = self.channels.index(channel_name)
            current_unit = xrkdll.get_channel_units(self.idxf, idxc)
            if current_unit != b'\xbb':
                current_unit = current_unit.decode('utf-8')
            else:
                current_unit = 'lambda'
            return current_unit
        except:
            return 0
            
    def channel_units_by_index(self, idxc):
        return xrkdll.get_channel_units(self.idxf, idxc).decode('utf-8')
    
    def channel_frequency(self,channel_name):
        try:
            idxc = self.channels.index(channel_name)
            sample_count = xrkdll.get_channel_samples_count(self.idxf, idxc)
            if sample_count > 0:
                laps = self.lap_count()
                current_start = ctypes.c_double(0)
                current_duration = ctypes.c_double(0)
                xrkdll.get_lap_info(self.idxf, laps-1, byref(current_start), byref(current_duration))
                total_time = round(current_start.value + current_duration.value,3)
                value = sample_count/total_time
                numbers = [1, 2, 5, 10, 20, 25, 50, 100, 200, 500, 1000]
                result = min(numbers, key=lambda x: abs(x - value))
            else:
                result = 0
            return result
        except:
            return 0

    def channel_frequency_by_index(self,idxc):
        sample_count = xrkdll.get_channel_samples_count(self.idxf, idxc)
        if sample_count > 0:
            laps = self.lap_count()
            current_start = ctypes.c_double(0)
            current_duration = ctypes.c_double(0)
            xrkdll.get_lap_info(self.idxf, laps-1, byref(current_start), byref(current_duration))
            total_time = round(current_start.value + current_duration.value,3)
            value = sample_count/total_time
            numbers = [1, 2, 5, 10, 20, 25, 50, 100, 200, 500, 1000]
            result = min(numbers, key=lambda x: abs(x - value))
        else:
            result = 0
        return result

    def channel_times_and_samples(self, channel_name):
        idxc = self.channels.index(channel_name)
        sample_count = self.channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_channel_samples(self.idxf, idxc, timeptr, sampleptr, sample_count)
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
        
    def channel_times_and_samples_by_index(self, idxc):
        sample_count = self.channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_channel_samples(self.idxf, idxc, timeptr, sampleptr, sample_count)
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
        
    def lap_channel_sample_count(self, channel_name, lap_number):
        idxl = lap_number - 1 
        try:
            idxc = self.channels.index(channel_name)
            return xrkdll.get_lap_channel_samples_count(self.idxf, idxl, idxc)
        except:
            return 0
            
    def lap_channel_sample_count_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        return xrkdll.get_lap_channel_samples_count(self.idxf, idxl, idxc)
        
    def lap_channel_times_and_samples(self, channel_name, lap_number):
        idxc = self.channels.index(channel_name)
        idxl = lap_number - 1
        sample_count = self.lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_lap_channel_samples(self.idxf, idxl, idxc, timeptr, sampleptr, sample_count)
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
        
    def lap_channel_times_and_samples_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        sample_count = self.lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_lap_channel_samples(self.idxf, idxl, idxc, timeptr, sampleptr, sample_count)
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
        
    ############################################################################
    ## GPS DATA CHANNEL MEHTODS
    ############################################################################  
  
    def GPS_channel_count(self):
        return xrkdll.get_GPS_channels_count(self.idxf)
        
    def GPS_channel_list(self):
        channel_names = []
        for i in range(self.GPS_channel_count()):
            channel_i = xrkdll.get_GPS_channel_name(self.idxf, i).decode('utf-8')
            channel_names.append(channel_i) 
        return channel_names
     
    def GPS_channel_sample_count(self, channel_name):
        try:
            idxc = self.GPS_channels.index(channel_name)
            return xrkdll.get_GPS_channel_samples_count(self.idxf, idxc)
        except:
            return 0

    def GPS_channel_sample_count_by_index(self, idxc):
        return xrkdll.get_GPS_channel_samples_count(self.idxf, idxc)
    
    def GPS_channel_units(self, channel_name):
        try:
            idxc = self.GPS_channels.index(channel_name)
            return xrkdll.get_GPS_channel_units(self.idxf, idxc).decode('utf-8')
        except:
            return 0
            
    def GPS_channel_units_by_index(self, idxc):
            return xrkdll.get_GPS_channel_units(self.idxf, idxc).decode('utf-8')

            
    def GPS_channel_times_and_samples(self, channel_name):
        idxc = self.GPS_channels.index(channel_name)
        sample_count = self.GPS_channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_GPS_channel_samples(self.idxf, idxc, timeptr, sampleptr, sample_count)
        
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
        
    def GPS_channel_times_and_samples_by_index(self, idxc):
        sample_count = self.GPS_channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_GPS_channel_samples(self.idxf, idxc, timeptr, sampleptr, sample_count)
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
        
    def GPS_lap_channel_sample_count(self, channel_name, lap_number):
        idxl = lap_number - 1 
        try:
            idxc = self.GPS_channels.index(channel_name)
            return xrkdll.get_lap_GPS_channel_samples_count(self.idxf, idxl, idxc)
        except:
            return 0
            
    def GPS_lap_channel_sample_count_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        return xrkdll.get_lap_GPS_channel_samples_count(self.idxf, idxl, idxc)
        
    def GPS_lap_channel_times_and_samples(self, channel_name, lap_number):
        idxc = self.GPS_channels.index(channel_name)
        idxl = lap_number - 1
        sample_count = self.GPS_lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_lap_GPS_channel_samples(self.idxf, idxl, idxc, timeptr, sampleptr, sample_count)
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
        
    def GPS_lap_channel_times_and_samples_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        sample_count = self.GPS_lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_lap_GPS_channel_samples(self.idxf, idxl, idxc, timeptr, sampleptr, sample_count)
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
        
    ############################################################################
    ## RAW GPS DATA CHANNEL MEHTODS
    ############################################################################  
        
    def GPS_raw_raw_channel_count(self):
        return xrkdll.get_GPS_raw_raw_channels_count(self.idxf)
        
    def GPS_raw_channel_count(self):
        return xrkdll.get_GPS_raw_channels_count(self.idxf)
        
    def GPS_raw_channel_list(self):
        channel_names = []
        for i in range(self.GPS_raw_channel_count()):
            channel_i = xrkdll.get_GPS_raw_channel_name(self.idxf, i).decode('utf-8')
            channel_names.append(channel_i) 
        return channel_names
     
    def GPS_raw_channel_sample_count(self, channel_name):
        try:
            idxc = self.GPS_raw_channels.index(channel_name)
            return xrkdll.get_GPS_raw_channel_samples_count(self.idxf, idxc)
        except:
            return 0

    def GPS_raw_channel_sample_count_by_index(self, idxc):
        return xrkdll.get_GPS_raw_channel_samples_count(self.idxf, idxc)
    
    def GPS_raw_channel_units(self, channel_name):
        try:
            idxc = self.GPS_raw_channels.index(channel_name)
            return xrkdll.get_GPS_raw_channel_units(self.idxf, idxc).decode('utf-8')
        except:
            return 0
            
    def GPS_raw_channel_units_by_index(self, idxc):
            return xrkdll.get_GPS_raw_channel_units(self.idxf, idxc).decode('utf-8')

    def GPS_raw_channel_times_and_samples(self, channel_name):
        idxc = self.GPS_raw_channels.index(channel_name)
        sample_count = self.GPS_raw_channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_GPS_raw_channel_samples(self.idxf, idxc, timeptr, sampleptr, sample_count)
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
        
    def GPS_raw_channel_times_and_samples_by_index(self, idxc):
        sample_count = self.GPS_raw_channel_sample_count_by_index(idxc)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_GPS_raw_channel_samples(self.idxf, idxc, timeptr, sampleptr, sample_count)
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
        
    def GPS_raw_lap_channel_sample_count(self, channel_name, lap_number):
        idxl = lap_number - 1 
        try:
            idxc = self.GPS_raw_channels.index(channel_name)
            return xrkdll.get_lap_GPS_raw_channel_samples_count(self.idxf, idxl, idxc)
        except:
            return 0
            
    def GPS_raw_lap_channel_sample_count_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        return xrkdll.get_lap_GPS_raw_channel_samples_count(self.idxf, idxl, idxc)
        
    def GPS_raw_lap_channel_times_and_samples(self, channel_name, lap_number):
        idxc = self.GPS_raw_channels.index(channel_name)
        idxl = lap_number - 1
        sample_count = self.GPS_raw_lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_lap_GPS_raw_channel_samples(self.idxf, idxl, idxc, timeptr, sampleptr, sample_count)
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
        
    def GPS_raw_lap_channel_times_and_samples_by_index(self, idxc, lap_number):
        idxl = lap_number - 1
        sample_count = self.GPS_raw_lap_channel_sample_count_by_index(idxc, lap_number)
        times = []
        samples = []
        timeptr = (ctypes.c_double * sample_count)()
        sampleptr = (ctypes.c_double * sample_count)()
        success = xrkdll.get_lap_GPS_raw_channel_samples(self.idxf, idxl, idxc, timeptr, sampleptr, sample_count)
        for i in range(sample_count):
            times.append(round(timeptr[i],3))
            samples.append(sampleptr[i])
        return [times, samples]
    
    
