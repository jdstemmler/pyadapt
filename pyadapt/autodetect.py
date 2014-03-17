#!/usr/bin/env python

"""Main read/write utility for the Py-ADAPT package.

Makes use of the :func:`read()` function to automatically detect the datastream
of the netCDF file and pass it to the appropriate 
:class:`pyadapt.datastreams.default.ARMCLASS` Class definition.

.. note::
    See the :func:`read()` function for more documentation
    
"""

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
    Automatically read the netCDF file passed into the routine and send it off
    to the appropriate Class definition to set up the data object.
    
    :param in_file: the filepath of the file you wish to look at
    :type in_file: str
    :returns: ARMCLASS Class object
    
    USEAGE:
    
    >>> import pyadapt
    >>> sounding = pyadapt.read('inputfile.nc')
    >>> sounding.plot()

    The Py-ADAPT package currently supports the following datastreams
        
        * SCATTERING
        * SFCMET
        * SOUNDINGS

    Supported File Types
        
        * .nc
        * .cdf
        * .cdf4
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
    
    # set the dstream variable to none
    dstream = None
    
    # try and overwrite dstream with datastream information found in the netCDF
    # files. So far .zeb_platform or .datastream have been found to contain
    # that information
    
    try:
        dstream = F.zeb_platform
    except AttributeError:
        pass
    
    try:
        dstream = F.datastream
    except AttributeError:
        pass
    
    if 'sonde' in dstream:          # Sounding File
        dat = SOUNDING(F, 'Upper Air Sounding')
    elif 'met' in dstream:       # Surface Meteorology File
        dat = SFCMET(F, 'Surface Meteorology File')
    elif 'aos' in F.dstream:
        dat = SCATTERING(F, 'Nephelometer File')
    else:
        raise IOError('Instrument Not Supported')
    
    #F.close()    
    return dat