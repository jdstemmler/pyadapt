import numpy
from .extras import ops

class SFCMET:
    '''
    Defines a SFCMET class for surface meteorology files
    '''
    
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
            
        self.data['datetime'] = ops.to_pydatetime(
                                self.data['time'],
                                self.units['time'])
        F.close()
    
    def plot(self, out=None):
        import matplotlib.pyplot as plt
        from .extras import windrose
        
        #...and adjust the legend box
        def set_legend(ax):
            l = ax.legend(borderaxespad=-4)
            plt.setp(l.get_texts(), fontsize=7)
        
        fig = plt.figure(figsize=(10,10), facecolor='w')
        rect = [0.1, 0.1, 0.8, 0.8]
        ax = windrose.WindroseAxes(fig, rect, axisbg='w')
        fig.add_axes(ax)
        
        ax.bar(self.data['wind_dir_vec_avg'],
               self.data['wind_spd_vec_avg'],
               opening=0.85, edgecolor='black',
               normed=True)
        
        plt.suptitle('Wind Rose')
        set_legend(ax)
        
        fig2 = plt.figure()
        ax = fig2.add_subplot(311)
        ax.plot(self.data['datetime'],
                self.data['precip_rate_mean'],
                'k.', label='mean')
        ax.set_ylabel('Precip Rate')
        ax.set_xticklabels('')
        ax.grid('on')
        
        ax = fig2.add_subplot(312)
        ax.plot(self.data['datetime'],
                self.data['wind_spd_vec_avg'],
                'k.', label='mean')
        ax.plot(self.data['datetime'],
                self.data['wind_spd_arith_max'],
                'b.', label='max')
        ax.legend(fontsize='xx-small', numpoints=1)
        ax.set_ylabel('Wind Speed')
        ax.set_xticklabels('')
        ax.grid('on')
        
        ax = fig2.add_subplot(313)
        ax.plot(self.data['datetime'],
                self.data['temp_mean'],
                'k-', label='mean')
        ax.set_ylabel('Temperature')
        ax.set_xlabel('Time (UTC)')
        ax.grid('on')