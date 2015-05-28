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

    def plot(self, altmax=None,
                 save_plot=False,
                 out_dir = '',
                 out_name = '',
                 out_fmt = 'png',
                 autoname = True,
                 **kwargs):
        """Plot a sounding for quick visualization

        :param altmax: Maximum altitude to show (m)
        :type altmax: float

        :param ptop: Uppermost pressure level for the plot
        :type ptop: float

        :param save_plot: Whether to save output
        :type save_plot: bool

        :param out_dir: Directory to save figures
        :type out_dir: string

        :param out_name: Name of the plot
        :type out_name: string

        :param out_fmt: Image format for the plot
        :type out_fmt: string

        :param autoname: Whether to automatically name plots
        :type autoname: bool

        As of right now, there are a lot of keywords input directly into the
        method. On the to-do list is to move those out into a **kwargs part
        of the plot method and set up a list of defaults so that passing
        something into kwargs overwrites the defaults instead of putting all
        the defaults into the method call.

        EXAMPLE:

        >>> S.plot(ptop=100, save_plot=True, autoname=True)

        Supported output types are anything that matplotlib can normally output,
        such as:

            * png
            * eps
            * pdf
        """

        from ..extras import skewt
        import os
        #import matplotlib.pyplot as plt

        ptop = kwargs.pop('ptop', 100.)
        skew = kwargs.pop('skew', 90)

        # create a mask for plotting of the altitude data
        if altmax and not ptop:
            vertmask = self.data['alt'] <= altmax
        elif ptop and not altmax:
            vertmask = self.data['pres'] >= ptop
        elif ptop and altmax:
            vertmask = self.data['pres'] >= ptop

        pbot = kwargs.pop('pbot', self.data['pres'][vertmask][0])

        # create the axes for the skew-t plot
        fig, ax, bx = skewt.skewt_axes(ptop=self.data['pres'][vertmask][-1],
                                       pbot=pbot,
                                       tmin=kwargs.pop('tmin', -10),
                                       tmax=kwargs.pop('tmax', 30),
                                       skew=skew)

        # plot a profile of temperature and pressure
        fig, ax = skewt.plot_profile(fig, ax,
                                self.data['tdry'],
                                self.data['pres'],
                                'r', label='tdry', skew=skew)
        # plot a profile of depoint temp and pressure
        fig, ax = skewt.plot_profile(fig, ax,
                                self.data['dp'],
                                self.data['pres'],
                                'b', label='dp', skew=skew)

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
        if save_plot:
            if autoname:
                out_str = 'sounding_%Y-%m-%dH%H.' + out_fmt
                out_name = self.file_datetime.strftime(out_str)
            fig.savefig(os.path.join(out_dir, out_name))
        else:
            fig.show()