import xarray as xr
from . import facilities as fc


class Dataset(object):

    def __init__(self, filename):

        ds = xr.open_dataset(filename)
        self.data = ds.data_vars
        self.coordinates = ds.coords
        for k, v in ds.attrs.items():
            setattr(self, k, v)

        self._str = ds.__repr__()

    def __repr__(self):
        return self._str

    def __str__(self):
        return self._str
