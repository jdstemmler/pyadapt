#!/usr/bin/env python

'''
Main read/write utility for the Py-ADAPT package.

Auto-detects the type of files supplied by the main read() function and
calls the appropriate read/write utility.

Usage:
    sounding = pyadapt.read('inputfile.nc')

Returns a 'sounding' object that can then be worked on.

Supported Instruments:
    SOUNDINGS

Supported File Types:
    *.nc
    *.cdf
    *.cdf4
'''

# import some basing things
import os
#from scipy.io import netcdf_file as nc
from netCDF4 import Dataset

from datastreams import *

# some setup things for smooth file operation
supported = ['nc', 'cdf', 'cdf4']

class IOError(Exception):
    pass

def read(in_file):
    '''
    Try to automatically read and return a data class appropriate for what
    is contained within the file.
    '''
    # check that the file exists
    if not os.path.isfile(in_file):
        raise IOError('Cannot Find File')
    
    # check that the file type is supported
    if os.path.basename(in_file).split('.')[-1] not in supported:
        raise IOError('Filetype Not Supported')
    
    # open the file for reading
    F = Dataset(in_file, 'r')
    
    # go throught the process of checking what the filetype is
    
    if 'sonde' in F.zeb_platform:          # Sounding File
        dat = SOUNDING(F, 'Upper Air Sounding')
    elif 'met' in F.zeb_platform:       # Surface Meteorology File
        dat = SFCMET(F, 'Surface Meteorology File')
    elif 'aos' in F.zeb_platform:
        dat = SCATTERING(F, 'Nephelometer File')
    else:
        raise IOError('Instrument Not Supported')
    
    #F.close()    
    return dat