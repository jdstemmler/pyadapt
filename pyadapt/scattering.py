import numpy, os, datetime
from extras import ops

class SCATTERING:
    '''
    Defines a SCATTERING class for surface nephelometer files
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
        self.kind = 'Surface Nephelometer File'
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
    
    def plot(self, plot_output = False, 
                    out_dir = '', 
                    out_name = '',
                    out_fmt = 'png',
                    autoname=True):
        
        import matplotlib.pyplot as plt
        
        fig = plt.figure(); fig.clf();
        ax = fig.add_subplot(211)
        bx = fig.add_subplot(212)
        
        col_prefix = [('Bs_B_','b'), ('Bs_G_','g'), ('Bs_R_','r')]
        
        for j,c in col_prefix:
            axvar = j+'Dry_1um_Neph3W_1'
            bxvar = j+'Dry_10um_Neph3W_1'
            ax.plot(self.data['datetime'], self.data[axvar], c+'-')
            bx.plot(self.data['datetime'], self.data[bxvar], c+'-')
        ax.set_ylabel('Scattering Coefficient')
        ax.set_title('Aerosol Total Light Scattering Coefficient\n' + 
                     'Ref. Neph., 1um Particle Diameter')
        bx.set_ylabel('Scattering Coefficient')
        bx.set_title('Ref. Neph., 10um Particle Diameter')
        
        ax.grid('on'); bx.grid('on')
        
        plt.tight_layout()
        
        if plot_output:
            if autoname:
                out_str = 'dry_scattering_%Y-%m-%d.' + out_fmt
                out_name = self.file_datetime.strftime(out_str)
            plt.savefig(out_dir + out_name)