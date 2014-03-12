import numpy, datetime, os
from extras import ops

class SOUNDING:
    """ Defines a SOUNDING class
    
    This particular class defines a sounding. It uses as input a netcdf file
    that has been detected as a sounding.
    
    """
    def __init__(self, F):
        self.data = {}
        self.keys = F.variables.keys()
        self.long_name = {}
        self.missing_value = {}
        self.dimensions = {}
        self.units = {}
        
        self.filename = os.path.basename(F.filename)
        self.site_id = F.site_id
        self.kind = 'Surface Meteorology File'
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
    
    def plot(self, altmax=10000, kind='simple', 
                plot_output=False,
                 out_dir = '',
                 out_name = '',
                 out_fmt = 'png',
                 autoname = True):
        ''' 
        plot a sounding for quick visualization
        
        you can set altmax (in meters) and an output file in out if you want.
        currently `kind` doesn't work, but will eventually support choosing
            between a normal height/temp plot and a skew-t
        
        example:
            S.plot(altmax=3000, out='sample_out.png')
        
        supported output types:
            anything that matplotlib can normally output, such as png, eps, pdf
        '''
        
        import matplotlib.pyplot as plt
        
        # create a mask for the altitude data
        altmask = self.data['alt'] < altmax
        
        # set up the plot
        f = plt.figure(); plt.clf()
        
        # create axes for the temperature and dewpoint plot
        ax = f.add_subplot(121)        
        if kind == 'simple':
            ax.plot(self.data['tdry'][altmask], 
                    self.data['alt'][altmask], 
                    'b-', label='Temp')
            ax.plot(self.data['dp'][altmask], 
                    self.data['alt'][altmask], 
                    'r-', label='Dewpoint')
            ax.legend()
            ax.set_ylim(top=altmax)
            ax.grid('on')
            
            ax.set_xlabel('Temperature (C)')
            ax.set_ylabel('Altitude (m)')
            ax.set_title(self.file_datetime.strftime(
                            'Sounding beginning %B %d %Y %H:%M'))
        
        # create axes for the RH plot
        ax = f.add_subplot(122)
        ax.plot(self.data['rh'][altmask], 
                self.data['alt'][altmask], 
                'k-', label='RelH')
        ax.legend()
        ax.grid('on')
        
        #plt.show()
        if plot_output:
            if autoname:
                out_str = 'sounding_%Y-%m-%dH%H.' + out_fmt
                out_name = self.file_datetime.strftime(out_str) 
            plt.savefig(out_dir + out_name)
        
        #plt.close(f)