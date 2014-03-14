def to_pydatetime(t, u):
    """Convert time array to python datetime objects
    
    :param t: time array from netCDF file
    :type t: array
    
    :param u: units for the time array
    :type u: str
    
    :returns: numpy array of datetime.datetime objects the same shape as
        the input time array
    """
    import datetime, numpy
    
    try:
        base = datetime.datetime.strptime(u,
        'seconds since %Y-%m-%d %H:%M:%S 0:00')
        dt = [base + datetime.timedelta(seconds=i) for i in t]
        return numpy.array(dt)
    except:
        print 'no datetime information found'
        return None