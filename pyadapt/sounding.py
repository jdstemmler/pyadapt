import numpy

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
                
        F.close()
    
    def plot(self, altmax=10000, kind='simple', out=None):
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
        
        # create axes for the RH plot
        ax = f.add_subplot(122)
        ax.plot(self.data['rh'][altmask], 
                self.data['alt'][altmask], 
                'k-', label='RelH')
        ax.legend()
        ax.grid('on')
        
        #plt.show()
        if out:
            plt.savefig(out)
        
        #plt.close(f)