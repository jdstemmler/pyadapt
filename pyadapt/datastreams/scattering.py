import numpy, os, datetime
from ..extras import ops
from default import ARMCLASS

class SCATTERING(ARMCLASS):
    '''
    Defines a SCATTERING class for surface nephelometer files
    ''' 
    def __init__(self):
        self.kind = 'Nephelometer Scattering Properties'
        
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
        ax.set_xticklabels('')
        ax.grid('on'); bx.grid('on')
        bx.set_xlabel(self.file_datetime.strftime('%B %d %Y'))
        
        plt.tight_layout()
        
        if plot_output:
            if autoname:
                out_str = 'dry_scattering_%Y-%m-%d.' + out_fmt
                out_name = self.file_datetime.strftime(out_str)
            plt.savefig(out_dir + out_name)