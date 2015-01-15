from ..extras import ops
from default import ARMCLASS

class SFCMET(ARMCLASS):
    """Defines a SFCMET class

    Inherits the attributes found in
    :class:`pyadapt.datastreams.default.ARMCLASS`

    This particular class defines a surface meteorology file.

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
        """Makes two figures to describe the surface meteorology data:

            * Windrose - polar histogram describing the wind speed and direction
                for the entire day
            * Timeseries - highlights the interday behavior of a selection of
                surface meteorology variables:

                * max wind speed
                * mean and max precipitation rates
                * temperature

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

        >>> S = pyadapt.datastreams.sfcmet.SFCMET(F, 'surface met file')
        >>> S.plot(plot_output=True, autoname=True)

        Supported output types are anything that matplotlib can normally output, such as:

            * png
            * eps
            * pdf
        """
        import matplotlib.pyplot as plt
        from ..extras import windrose
        import os

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
            plt.savefig(os.path.join(out_dir, out_name))

        fig2 = plt.figure()
        ax = fig2.add_subplot(311)
        ax.plot(self.data['datetime'],
                self.data['precip_rate_mean'],
                'k.', label='mean')
        ax.set_ylabel('Precip Rate'+'\n($'+self.units['precip_rate_mean']+'$)')
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
        ax.set_ylabel('Wind Speed'+'\n($'+self.units['wind_spd_vec_avg']+'$)')
        ax.set_xticklabels('')
        ax.grid('on')

        ax = fig2.add_subplot(313)
        ax.plot(self.data['datetime'],
                self.data['temp_mean'],
                'k-', label='mean')
        ax.set_ylabel('Temperature'+'\n($'+self.units['temp_mean']+'$)')
        ax.set_xlabel('Time (UTC) '+self.file_datetime.strftime('%B %d %Y'))
        ax.grid('on')

        ti_str = self.file_datetime.strftime('Surface Met Info for %B %d %Y\n')
        plt.suptitle(ti_str)
        #plt.tight_layout()

        if plot_output:
            if autoname:
                out_str = 'sfc_vars_%Y-%m-%d.' + out_fmt
                out_name = self.file_datetime.strftime(out_str)

            plt.savefig(os.path.join(out_dir, out_name))