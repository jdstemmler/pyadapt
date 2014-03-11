import numpy, os, datetime
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
        self.file_datetime = datetime.datetime(1970, 1, 1) + datetime.timedelta(
                                seconds = self.data['base_time'].tolist())
        F.close()
    
    def plot(self, plot_output = False, 
                    out_dir = '', 
                    out_name = '',
                    out_fmt = 'png',
                    autoname=True):
        import matplotlib.pyplot as plt
        from .extras import windrose
        
        fig = plt.figure(facecolor='w')
        rect = [0.15, 0.15, 0.7, 0.7]
        ax = windrose.WindroseAxes(fig, rect, axisbg='w')
        fig.add_axes(ax)
        
        ax.bar(self.data['wind_dir_vec_avg'],
               self.data['wind_spd_vec_avg'],
               opening=0.85, edgecolor='black',
               normed=True)
        
        ti_str1 = self.file_datetime.strftime('Wind Rose for %B %d %Y\n')
        ti_str2 = self.data['datetime'][0].strftime('%H:%M - ')
        ti_str3 = self.data['datetime'][-1].strftime('%H:%M')

        plt.suptitle(ti_str1 + ti_str2 + ti_str3)
        l = ax.legend(loc='lower left', bbox_to_anchor = (1., 0),
                      fontsize='x-small')
        
        if plot_output:
            if autoname:
                out_str = 'windrose_%Y-%m-%d.' + out_fmt
                out_name = self.file_datetime.strftime(out_str)
            plt.savefig(out_dir + out_name)
        
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
        
        ti_str = self.file_datetime.strftime('Surface Met Info for %B %d %Y\n')
        plt.suptitle(ti_str)
        plt.tight_layout()
        
        if plot_output:
            if autoname:
                out_str = 'sfc_vars_%Y-%m-%d.' + out_fmt
                out_name = self.file_datetime.strftime(out_str)
            plt.savefig(out_dir + out_name)