import os

class Datastream(object):

    def __init__(self, filename):

        if isinstance(filename, str):
            _is_file = os.path.isfile(filename)
            _is_dir  = os.path.isdir(filename)

            self.filename = os.path.abspath(filename)

    def __str__(self):
        return "Datastrem Object for \n - {}".format(self.filename)
