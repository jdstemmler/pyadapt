import os
import re
from ._prettytable import PrettyTable, ALL
from netCDF4 import Dataset


def _check_variable_for_exclude(exclude, name):

    return sum(len(re.findall(e, name)) for e in exclude) > 0


def list_file_attributes(filename, exclude=None):

    if not os.path.exists(filename):
        raise FileNotFoundError("{} Not Found".format(filename))

    if os.path.isdir(filename):
        raise IsADirectoryError("{} is a Directory".format(filename))

    if not os.path.isfile(filename):
        raise FileNotFoundError("HOW??")

    with Dataset(filename, 'r') as D:

        p = PrettyTable(['Name', 'Units', 'Dimensions'])
        p.align = 'l'
        p.hrules = ALL

        for name, variable in D.variables.items():

            if (exclude is not None) & (isinstance(exclude, (list, tuple))):
                if _check_variable_for_exclude(exclude, name):
                    continue
                else:
                    pass
            else:
                pass

            p.add_row(["{}\n  '{}'".format(getattr(variable, 'long_name', name).upper(), name),
                       getattr(variable, 'units', None),
                       getattr(variable, 'dimensions', None)
                       ])

        print(p.get_string(sortby="Name"))
