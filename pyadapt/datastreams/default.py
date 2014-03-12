import os, datetime, numpy
from ..extras import ops

class ARMCLASS:
    
    def __init__(self, F, kind):
        self.data = {}
        self.keys = F.variables.keys()
        self.long_name = {}
        self.missing_value = {}
        self.dimensions = {}
        self.units = {}
        self.kind = kind
        
        self.filename = os.path.basename(F.filename)
        self.site_id = F.site_id
        self.sample_int = F.sample_int
        self.comment = F.comment
        
        for i in F.variables.keys():
            #self.data[i] = F.variables[i].data
            self.long_name[i] = F.variables[i].long_name
            self.dimensions[i] = F.variables[i].dimensions
            self.units[i] = F.variables[i].units
            
            # sometimes missing_value data isn't there
            try:
                self.missing_value[i] = F.variables[i].missing_value
                self.data[i] = numpy.ma.masked_values(
                                F.variables[i].data,
                                F.variables[i].missing_value)
            except AttributeError:
                self.data[i] = F.variables[i].data
        
        self.data['datetime'] = ops.to_pydatetime(
                                self.data['time'],
                                self.units['time'])        
        #self.file_datetime = datetime.datetime(1970, 1, 1)+datetime.timedelta(
        #                        seconds = self.data['base_time'].tolist())
        self.file_datetime = datetime.datetime.strptime(self.units['time'],
                        'seconds since %Y-%m-%d %H:%M:%S 0:00')
        
        F.close()