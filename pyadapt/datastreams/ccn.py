from ..extras import ops
from default import ARMCLASS

class CCN(ARMCLASS):
    """Defines a CCN class
    
    Inherits the attributes found in 
    :class:`pyadapt.datastreams.default.ARMCLASS`
    
    This particular class defines a ccn particle counter file.
    
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
        """Makes one figure to describe the ccn amount data:
        
            * Timeseries - highlights the interday behavior of the ccn amount
              as a function of supersaturation. The timeseries shows ccn
              particle counts for three supersaturation ranges:
            
               * 0.0 - 0.15%
               * 0.3 - 0.45%
               * 0.75 - 1.0%
        
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
        
        >>> S = pyadapt.datastreams.ccn.CCN(F, 'ccnfile.nc')
        >>> S.plot(plot_output=True, autoname=True)
        
        Supported output types are anything that matplotlib can normally output,
        such as:
            
            * png
            * eps
            * pdf
        """
        import matplotlib.pyplot as plt
        
        ss_vals = [[0.0, 0.15], [0.4, 0.6], [0.75, 1.0]]
        cols = ['blue', 'g', 'firebrick']
        
        ccn = self.data['N_CCN']
        ss = self.data['CCN_ss_set']
        dt = self.data['datetime']
        
        fig = plt.figure(figsize=(10,6))
        ax = fig.add_subplot(111)
        
        for i,c in zip(ss_vals, cols):
            mask = (ss > i[0]) & (ss < i[1])
            ax.plot(dt[mask], ccn[mask], c=c, marker='.', ls='none',
                    label = '{:1.2f}<ss<{:1.2f}'.format(i[0], i[1]))
        
        ax.grid('on')
        ax.legend(numpoints=1, fontsize='xx-small', ncol=3, 
                  title='ss range')
        
        ax.set_ylabel('CCN'+'\n($'+self.units['N_CCN']+'$)')
        ax.set_xlabel('Time (UTC) ' + self.file_datetime.strftime('%B %d %Y'))
        ax.set_title('Cloud Droplet Number Concentration')