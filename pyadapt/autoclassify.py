from pyadapt.baseclasses import _TimeSeries1D


def _autoclass(filename):
    pass


def Datastream(filename, varlist=None, keep_nan_vars=False, **kwargs):

    if varlist is None:
        raise NotImplementedError("Sorry, Autodetection of variables is not implemented yet")

    kwargs.update({'keep_nan_vars': keep_nan_vars})

    return _TimeSeries1D(filename, varlist=varlist, **kwargs)

