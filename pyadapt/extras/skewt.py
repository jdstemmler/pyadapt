import numpy
from numpy import log10

def skewfactor(p, skew, ref=1000.):
    
    return (log10(p) - log10(ref)) * skew

def skewt_axes(tmin = -40, tmax = 30,
               ptop = 550., pbot = 1050.,
               skew = 100.,
               figsize=(10,10)):

    import matplotlib.pyplot as plt
    
    # some defaults
    #tmin = -40; tmax = 30; ptop = 550; pbot = 1050; skew=100; figsize=(10,10)
    
    # bases some things off of a reference pressure of 1000hPa
    rpres = 1000.
    
    # skew is defined as the temperature difference between 1000 and 100 mb
    # if ptop and pbottom are different, need to adjust skew
    #skew = skew * (pbot - ptop)/900.
    
    # set up the temperature and pressure grids
    temp = numpy.linspace(tmin, tmax, 70)
    pres = numpy.linspace(ptop, pbot, 100)
    plev = numpy.linspace(log10(ptop), log10(pbot), 100)
    
    # determine a skew factor for each row of the grid
    skf = skewfactor(10**plev, skew)
    
    # mesh it!
    tempgrid, plevgrid = numpy.meshgrid(temp, plev)
    xx, skewgrid = numpy.meshgrid(temp, skf)
    xx, skewpres = numpy.meshgrid(temp, pres)
    
    # apply the skewfactor to the temperature grid
    tempskew = tempgrid + skewgrid
    
    # create a potential temperature grid
    thetagrid = (tempskew + 273.15) * (rpres / skewpres)**(287/1005.7)
    
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
    
    TH = ax.contour(temp, -1*plev, thetagrid,
                    colors='green', linestyles='dashed')
    # set the appropriate yticks and limits
    # yticks are referenced from 1000 and spaced every 50mb
    ax.set_yticks(-1*log10(numpy.arange(1000, 50, -50.)))
    ax.set_yticklabels(['{:4.0f}'.format(i) for i in 
                        numpy.arange(1000, 50, -50.)])
    
    ax.set_ylim(bottom = -1*log10(pbot), top = -1*log10(ptop))
    
    ax.plot([tmin, tmax], [-1*log10(rpres), -1*log10(rpres)], 'k-', 
                linewidth=2)
    
    T.clabel(inline=True, fontsize='x-small', fmt='%1.0f')
    TH.clabel(inline=True, fontsize='x-small', fmt='%1.0f')
    
    ax.set_xlabel('Temperature (C) at 1000 hPa')
    ax.set_ylabel('Pressure (hPa)')
    
    bx1 = fig.add_axes([0.8, 0.1, 0.1, 0.8])
    bx1.set_yticks([])
    bx = bx1.twinx()
    bx.set_xticks([])
    bx.set_ylabel('Altitude (km)')
    bx.minorticks_on()
    bx.grid('on', which='both', axis='y')
    
    return fig, ax, bx

def transform_profile(temperature, pressure, skew=100.):
    from numpy import log10
    pres = -1 * log10(pressure)
    temp = temperature - skewfactor(pressure, skew)
    
    return temp,  pres

def plot(fig, ax, t, p, c='r', label=''):
    
    xlim = ax.get_xlim()
    
    ax.plot(t, p, c+'-', label=label)
    ax.set_xlim(xlim)
    ax.legend(fontsize='xx-small')
    
    return fig, ax