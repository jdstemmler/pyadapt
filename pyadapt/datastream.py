import os


class _BaseDatastream(object):

    def __init__(self, filename, **kwargs):

        if isinstance(filename, str):
            self.filename = os.path.abspath(filename)
        elif isinstance(filename, (list, tuple)):
            self.filename = (os.path.abspath(f) if os.path.isfile(f) else None for f in filename)
        else:
            self.filename = filename

        self.name = "Generic Datastream"

    def __str__(self):
        return "{} for \n - {}".format(self.name, os.path.basename(self.filename))


class _SurfaceMet(_BaseDatastream):

    def __init__(self, filename, **kwargs):
        super(_SurfaceMet, self).__init__(filename, **kwargs)
        self.name = "Surface Meteorology"


class _AerosolObservingSystem(_BaseDatastream):

    def __init__(self, filename, **kwargs):
        super(_AerosolObservingSystem, self).__init__(filename, **kwargs)
        self.name = "Aerosol Observing System"


def _find_stream_from_keyword(s):
    if s.lower() in ('met', 'sfcmet', 'meteorology'):
        ds = _SurfaceMet
    else:
        raise NotImplementedError("Data type {} not supported".format(s))

    return ds


def _find_stream_from_filename(f):
    parts = os.path.basename(f).split('.')
    meta = parts[0]

    if 'met' in meta:
        return _SurfaceMet
    elif 'aos' in meta:
        return _AerosolObservingSystem


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


def Datastream(filename, stream=None, **kwargs):
    """Select the correct Datastream to pass back to the user"""

    f = _validate_filename(filename)

    if (stream is not None) & isinstance(stream, str):

        ds = _find_stream_from_keyword(stream)

    else:

        ds = _find_stream_from_filename(f)

    return ds(filename, **kwargs)
