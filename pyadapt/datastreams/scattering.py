from ..extras import ops
from default import ARMCLASS

class SCATTERING(ARMCLASS):
    """Defines a SCATTERING class
    
    Inherits the attributes found in 
    :class:`pyadapt.datastreams.default.ARMCLASS`
    
    This particular class defines a nephelometer aerosol scattering file.
    
    INPUTS
    
    :param F: netCDF4 Dataset Object
    :type F: netCDF4.Dataset
    :param kind: String describing the type of data
    :type kind: str

    :returns: ARMCLASS object
    """ 
        
    def plot(self, plot_output = False, 
                    out_dir = '', 
                    out_name = '',
                    out_fmt = 'png',
                    autoname=True):
        """Makes one figure to describe the nephelometer scattering data:
        
            * Timeseries - highlights the interday behavior of the dry
              aerosol scattering properties. Each panel shows the aerosol 
              scattering at a particular cutoff size for
                
                * red wavelength
                * blue wavelength
                * green wavelength
        
        :param plot_output: Whether to save output
        :type plot_output: bool
        
        :param out_dir: Directory to save figures
        :type out_dir: string
        
        :param out_name: Name of the plot
        :type out_name: string
        
        :param out_fmt: Image format for the plot
        :type out_fmt: string
        
        :param autoname: Whether to automatically name plots
        :type autoname: bool
        
        EXAMPLE:
        
        >>> S = pyadapt.datastreams.scattering.SCATTERING(F, 'surface met file')
        >>> S.plot(plot_output=True, autoname=True)
        
        Supported output types are anything that matplotlib can normally output, such as:
            
            * png
            * eps
            * pdf
        """
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