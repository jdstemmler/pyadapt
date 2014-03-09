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
from scipy.io import netcdf_file as nc

from . import read_sounding

# some setup things for smooth file operation
supported = ['nc', 'cdf', 'cdf4']

class IOError(Exception):
    pass

def read(in_file):
    
    # check that the file exists
    if not os.path.isfile(in_file):
        raise IOError('Cannot Find File')
    
    # check that the file type is supported
    if os.path.basename(in_file).split('.')[0] not in supported:
        raise IOError('Filetype Not Supported')