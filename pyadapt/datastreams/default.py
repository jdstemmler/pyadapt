import os, datetime, numpy
from ..extras import ops

class ARMCLASS:
    """Defines the default ARMCLASS for the different data streams.
    This generally isn't called directlly, but rather used as a template
    for the other classes and their plotting routines.
    
    INPUTS
    
    :param F: netCDF4 Dataset Object
    :type F: netCDF4.Dataset
    :param kind: String describing the type of data
    :type kind: str

    :returns: ARMCLASS Class
    
    The ARMCLASS Class contains all the data from the original netCDF file
    that was input into the individual routines. A description of each of the
    attributes is as follows.
    
    :.keys: a list containing all the data keys
    :.data: dictionary containing the actual data. The keys for the dict are
        found in *self.keys*
    :.long_name: dict containing the long_name description of the variable
    :.missing_value: dict containing the missing_values for masking
    :.dimensions: dict with the dimensions for each of the data variables
    :.units: dict containing the units for each of the data variables
    :.kind: string describing the kind of data this is (eg sounding, sfcmet...)
    :.site_id: site ID for the data file
    :.comment: any comments added by the file creator
    :.datetime: an array of datetime objects the same shape as the 'time'
    
    >>> ARM = pyadapt.datastreams.default.ARMCLASS(F, kind='example kind')
    # to get a variable called 'temperature' from ARM use:
    >>> temperature = ARM.data['temperature']
    # you can also see the units of 'temperature'
    >>> ARM.units['temperature']
    u'degrees celcius'
    
    .. note::
        You will not usually call a particular ARMCLASS by name. Rather, the
        preferred method is to use the :mod:`pyadapt.autodetect.read()` function 
        which automatically calls the appropriate ARMCLASS for you. 
    """
    def __init__(self, F, kind):
        self.data = {}
        self.keys = F.variables.keys()
        self.long_name = {}
        self.missing_value = {}
        self.dimensions = {}
        self.units = {}
        self.kind = kind
        
        #self.filename = os.path.basename(F.filename)
        self.site_id = F.site_id
        #self.sample_int = F.sample_int
        try:
            self.comment = F.comment
        except AttributeError:
            pass
            
        for i in F.variables.keys():
            #self.data[i] = F.variables[i].data
            self.long_name[i] = F.variables[i].long_name
            self.dimensions[i] = F.variables[i].dimensions
            self.units[i] = F.variables[i].units
            
            # sometimes missing_value data isn't there
            try:
                self.missing_value[i] = F.variables[i].missing_value
                self.data[i] = numpy.ma.masked_values(
                                F.variables[i][:],
                                F.variables[i].missing_value)
            except AttributeError:
                self.data[i] = F.variables[i][:]
        
        self.data['datetime'] = ops.to_pydatetime(
                                self.data['time'],
                                self.units['time'])        
        #self.file_datetime = datetime.datetime(1970, 1, 1)+datetime.timedelta(
        #                        seconds = self.data['base_time'].tolist())
        self.file_datetime = datetime.datetime.strptime(self.units['time'],
                        'seconds since %Y-%m-%d %H:%M:%S 0:00') + \
                        datetime.timedelta(seconds=self.data['time'][0])
        
        F.close()