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
        
    def plot(self, altmax=10000, pmax = None, 
                 kind='skew-t', 
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
        
        Supported output types are anything that matplotlib can normally output, 
        such as:
            
            * png
            * eps
            * pdf
        """
        
        from ..extras import skewt
        #import matplotlib.pyplot as plt
        
        # create a mask for plotting of the altitude data
        if altmax and not pmax:
            vertmask = self.data['alt'] <= altmax
        elif pmax and not altmax:
            vertmask = self.data['pres'] <= pmax
        elif pmax and altmax:
            vertmask = self.data['alt'] <= altmax
        
        
        # create the axes for the skew-t plot
        fig, ax, bx = skewt.skewt_axes(ptop = self.data['pres'][vertmask][-1],
                                       pbot = self.data['pres'][vertmask][0], 
                                       tmin = 0)
        
        # plot a profile of temperature and pressure
        fig, ax = skewt.plot_profile(fig, ax,
                                self.data['tdry'], 
                                self.data['pres'],
                                'r', label='tdry')
        # plot a profile of depoint temp and pressure
        fig, ax = skewt.plot_profile(fig, ax,
                                self.data['dp'], 
                                self.data['pres'], 
                                'b', label='dp')
        
        # plot the vertical profile of winds
        fig, bx = skewt.plot_wind(fig, bx, vertmask,
                                self.data['u_wind'],
                                self.data['v_wind'],
                                self.data['alt'],
                                skip=50)
        
        # set the title of the plot
        fig.suptitle(self.file_datetime.strftime(
                          'Sounding beginning %B %d %Y %H:%M'),
                          fontsize=16)
        
        # save some plot output if desired
        if plot_output:
            if autoname:
                out_str = 'sounding_%Y-%m-%dH%H.' + out_fmt
                out_name = self.file_datetime.strftime(out_str) 
            fig.savefig(out_dir + out_name)