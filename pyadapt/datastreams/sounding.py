import numpy, os, datetime
from ..extras import ops
from default import ARMCLASS

class SOUNDING(ARMCLASS):
    """Defines a SOUNDING class
    
    Inherits the attributes found in
    :class:`pyadapt.datastreams.default.ARMCLASS`
    
    This particular class defines a sounding. It uses as input a netcdf file
    that has been detected as a sounding.
    
    INPUTS
    
    :param F: netCDF4 Dataset Object
    :type F: netCDF4.Dataset
    :param kind: String describing the type of data
    :type kind: str

    :returns: ARMCLASS object
    """
        
    def plot(self, altmax=10000, kind='simple', 
                plot_output=False,
                 out_dir = '',
                 out_name = '',
                 out_fmt = 'png',
                 autoname = True):
        """Plot a sounding for quick visualization
        
        :param altmax: Maximum altitude to show (m)
        :type altmax: float
        
        :param kind: What kind of plot to make (simple, skew-t)
        :type kind: str
        
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
        
        .. note:: 
            Currently the 'kind' keyword has no effect, so leave it as simple
        
        EXAMPLE:
        
        >>> S.plot(altmax=3000, plot_output=True, autoname=True)
        
        Supported output types are anything that matplotlib can normally output, such as:
            
            * png
            * eps
            * pdf
        """
        
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
            ax.legend(fontsize='x-small')
            ax.set_ylim(top=altmax)
            ax.grid('on')
            
            ax.set_xlabel('Temperature (C)')
            ax.set_ylabel('Altitude (m)')
            plt.suptitle(self.file_datetime.strftime(
                            'Sounding beginning %B %d %Y %H:%M'))
        
        # create axes for the RH plot
        ax = f.add_subplot(122)
        ax.plot(self.data['rh'][altmask], 
                self.data['alt'][altmask], 
                'k-', label='RelH')
        ax.legend(fontsize='x-small')
        ax.grid('on')
        ax.set_yticklabels('')
        ax.set_xlabel('RH (%)')
        
        #plt.show()
        if plot_output:
            if autoname:
                out_str = 'sounding_%Y-%m-%dH%H.' + out_fmt
                out_name = self.file_datetime.strftime(out_str) 
            plt.savefig(out_dir + out_name)
        
        #plt.close(f)