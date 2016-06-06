from .baseclasses import _TimeSeries1D


def _autoclass(filename):
    pass


def Datastream(filename, varlist=None):

    if varlist is None:
        raise NotImplementedError("Sorry, Autodetection of variables is not implemented yet")

    return _TimeSeries1D(filename, varlist=varlist)