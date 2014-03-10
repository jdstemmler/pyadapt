def to_pydatetime(t, u):
    import datetime, numpy
    
    try:
        base = datetime.datetime.strptime(u,
        'seconds since %Y-%m-%d %H:%M:%S 0:00')
        dt = [base + datetime.timedelta(seconds=i) for i in t]
        return numpy.array(dt)
    except:
        print 'no datetime information found'
        return None