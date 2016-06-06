import os
import numpy as np
import pandas as pd
from netCDF4 import Dataset, num2date


def _validate_filename(f):

    if isinstance(f, (list, tuple)):
        raise NotImplementedError("Lists and Tuples are not yet supported")

    if not os.path.exists(f):
        raise FileNotFoundError("File {} does not exist".format(f))

    if os.path.isdir(f):
        raise NotImplementedError("Directories are not yet supported")

    if not isinstance(f, str):
        raise TypeError("Input must be a string at this point")

    return os.path.abspath(f)


def _validate_varlist(v):

    if isinstance(v, str):
        return {v: v}

    elif isinstance(v, (list, tuple)):
        return {k: k for k in v}

    elif isinstance(v, dict):
        return v


class _TimeSeries1D(object):

    def __init__(self, filename, varlist=None, keep_nan_vars=True, **kwargs):

        self.filename = _validate_filename(filename)
        self.varlist = _validate_varlist(varlist)

        self.data = self.init_data()

        self._keep_nan_vars = keep_nan_vars

        for k, v in kwargs:
            setattr(self, k, v)

    def __str__(self):
        return "{}\n  *{}".format(os.path.basename(self.filename), '\n  *'.join(self.varlist))

    def init_data(self):

        data = {}

        with Dataset(self.filename, 'r') as D:
            time = D.variables.get('time', None)
            time_units = getattr(time, 'units', None)

            if (time is not None) & (time_units is not None):
                t = num2date(time[:], time_units)
            else:
                raise AttributeError('"Time" parameter in datastream either does not exist or not properly formatted')

            for k, v in self.varlist.items():
                tmp = D.variables.get(v)
                if tmp is not None:
                    data[k] = tmp[:]
                else:
                    if self._keep_nan_vars:
                        data[k] = np.repeat(np.nan, len(t))
                    else:
                        continue

        return pd.DataFrame(data, index=t)
