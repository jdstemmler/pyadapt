import numpy
from numpy import log10

def skewfactor(p, skew, ref=1000.):
    """Calculates the skew factor for a given pressure and skewness
    
    :param p: pressure
    :type p: float or array of float
    
    :param skew: skewness of the plot
    :type skew: float
    
    :param ref: reference pressure level. keep it at 1000.
    :type ref: float
    
    :returns skewfactor: skewness of the skew-t plot
    
    """
    return (log10(p) - log10(ref)) * skew

def skewt_axes(tmin = -40, tmax = 30,
               ptop = 550., pbot = 1050.,
               skew = 100.,
               figsize=(10,10)):
    """Creates axes for the skew-t and wind profile plot.
    
    :param tmin: Minimum temperature (c) along 1000 hPa
    :type tmin: float
    
    :param tmax: Maximum temperature (c) along 1000 hPa
    :type tmax: float
    
    :param ptop: Pressure (hPa) for the top of the figure
    :type ptop: float
    
    :param pbot: Pressure (hPa) for the bottom of the figure
    :type pbot: float
    
    :param skew: Skewness of the plot (larger number, more skew)
    :type skew: float
    
    :param figsize: size of the figure
    :type figsize: tuple(int, int)
    
    .. note::
       pbot should be larger (lower) or equal to 1000 hPa for best results. 
    
    :returns fig: figure reference
    :returns ax: axis reference for the skew-t
    :returns bx: axis reference for the wind profile
    
    This skew-t axis generator is a little different than some of the more
    complex routines out there. In this case, coordinates on the grid are
    transformed for ease of plotting.
    
        * pbot and ptop are transformed into -1*log10(p) units so that pbot
          is on the bottom and ptop is on top, and that the spacing of the 
          pressure grid is in log space (but the axes are linear).
        * tmin and tmax are used to define the temperature range at the
          reference pressure of 1000 hPa. Plotting the temperatures requires
          transforming the value down to the reference level based on the
          pressure and skewness associated with the temperature.
    
    Isobars, isotherms, and dry adiabats are computed as a grid which fills
    the axis space and are then contoured. 
    
    For plotting of the actual sounding data, the input temperature and pressure
    must be transformed using the same method as the underlying grid, and so
    must be passed into the :meth:`transform_profile` method, but that should
    all get handled by the :meth:`plot_profile` method.
    """
    
    import matplotlib.pyplot as plt
    
    # some defaults
    #tmin = -30; tmax = 40; ptop = 100; pbot = 1050; skew=75; figsize=(10,10)
    
    # bases some things off of a reference pressure of 1000hPa
    rpres = 1000.
    
    # set up the temperature and pressure grids
    temp = numpy.linspace(tmin, tmax, 70)
    plev = numpy.linspace(log10(ptop), log10(pbot), 100)
    pres = 10**plev
    
    # determine a skew factor for each row of the grid
    skf = skewfactor(10**plev, skew)
    
    # mesh it!
    tempgrid, plevgrid = numpy.meshgrid(temp, plev)  # temp and log pressure lev
    xx, skewgrid = numpy.meshgrid(temp, skf)         # skew factor grid
    xx, presgrid = numpy.meshgrid(temp, pres)        # pressure grid
    
    # apply the skewfactor to the temperature grid
    tempskew = tempgrid + skewgrid
    
    # create a potential temperature grid
    thetagrid = (tempskew + 273.15) * (rpres / presgrid)**(287/1005.7)
    
    # generate the figure
    fig = plt.figure(figsize=figsize)
    ax = fig.add_axes([0.1, 0.1, 0.7, 0.8])
    
    # contour the temperature grid
    T = ax.contour(temp, -1*plev, tempskew, 
            levels=numpy.arange(tmin-skew, tmax, 10.),
            colors = 'orange',
            linestyles='solid')
    
    # contour the pressure grid
    P = ax.contour(temp, -1*plev, plevgrid,
            levels = log10(numpy.arange(1000, 100, -50)),
            colors='orange', 
            linestyles='solid')
    
    # contour the potential temprature grid
    TH = ax.contour(temp, -1*plev, thetagrid,
                    levels = numpy.arange(tmin-skew+273.15, 
                                          thetagrid.max(), 10.),
                    colors='green', linestyles='dashed')
                    
    # set the appropriate yticks and limits
    # yticks are referenced from 1000 and spaced every 50mb
    ax.set_yticks(-1*log10(numpy.arange(1000, 50, -50.)))
    ax.set_yticklabels(['{:4.0f}'.format(i) for i in 
                        numpy.arange(1000, 50, -50.)])
    
    ax.set_ylim(bottom = -1*log10(pbot), top = -1*log10(ptop))
    
    # plot a black line at 1000 hPa
    ax.plot([tmin, tmax], [-1*log10(rpres), -1*log10(rpres)], 'k-', 
                linewidth=2)
    
    # set label formatting for the contours
    T.clabel(inline=True, fontsize='x-small', fmt='%1.0f')
    TH.clabel(inline=True, fontsize='x-small', fmt='%1.0f')
    
    # set up some labels
    ax.set_xlabel('Temperature (C) at 1000 hPa')
    ax.set_ylabel('Pressure (hPa)')
    
    # generate the axes for the wind profile
    bx1 = fig.add_axes([0.8, 0.1, 0.1, 0.8])
    bx1.set_yticks([])
    bx = bx1.twinx()
    bx.set_xticks([])
    bx.set_ylabel('Altitude (km)')
    #bx.minorticks_on()
    #bx.grid('on', which='both', axis='y')
    
    return fig, ax, bx

def transform_profile(temperature, pressure, skew=100.):
    """Transforms a temperature profile using its pressure and skewness
    
    :param temperature: temperature profile or single value
    :type temperature: float or array(floats)
    
    :param pressure: pressure for associated temperature
    :type pressure: float or array(floats)
    
    :param skew: skewness of the skew-t
    :type skew: float
    
    :returns temp: the transformed temperature value
    :returns pres: the transformed pressure value
    
    """
    from numpy import log10
    pres = -1 * log10(pressure)
    temp = temperature - skewfactor(pressure, skew)
    
    return temp,  pres

def plot_profile(fig, ax, t, p, c='r', label='', skew=100.):
    """Plots a temperature profile on the supplied axes
    
    :param fig: the figure generated by :meth:`skewt_axes`
    :param ax: the skew-t axis generated by :meth:`skewt_axes`
    
    :param t: temperature profile (untransformed)
    :param p: pressure profile
    
    :param c: the color of the line to plot
    :param label: label for the legend
    :param skew: skewness of the skew-t grid
    
    :returns fig: the skew-t figure
    :returns ax: the skew-t axis after plotting
    """
    xlim = ax.get_xlim()
    
    temp, pres = transform_profile(t, p, skew)
    
    ax.plot(temp, pres, c+'-', label=label)
    ax.set_xlim(xlim)
    ax.legend(fontsize='xx-small')
    
    return fig, ax

def plot_wind(fig, bx, mask, u, v, a, skip=50):
    """Plots a wind profile on the supplied axes
    
    :param fig: the figure generated by :meth:`skewt_axes`
    :param bx: the wind profile axis generated by :meth:`skewt_axes`
    
    :param mask: mask of booleans for limiting the vertical extent
    
    :param u: U component of the wind
    :param v: V component of the wind
    :param a: altitude corresponding to each of the U,V values
    
    :param skip: skipping factor for thinning out the wind barbs
    
    """
    bx.barbs(numpy.zeros(len(a[mask][::skip])),
             a[mask][::skip]/1000.,
             u[mask][::skip],
             v[mask][::skip])
    
    bx.set_ylim((a[mask][0]/1000., a[mask][-1]/1000.))
    bx.minorticks_on()
    bx.grid('on', which='both', axis='y')
    
    return fig, bx