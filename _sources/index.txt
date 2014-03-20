.. Py-ADAPT documentation master file, created by
   sphinx-quickstart on Thu Mar 13 16:14:17 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Py-ADAPT's documentation!
====================================
.. toctree::
   :maxdepth: 4

   pyadapt

Quickstart Guide
----------------
Py-ADAPT is the Python ARM Data Analysis and Plotting Toolkit, useful for quickly accessing and plotting data available from the ARM archive. Not all datastreams are supported yet, but new ones are being added as this package scales up.

The code repository is hosted on github. It can be found here: http://github.com/jstemmler/pyadapt

To get up and running quickly, follow these steps.

Clone and Install
+++++++++++++++++
First you need to clone the repository from github onto your local machine. You can do this by issuing the following command from the directory that you would like to install pyadapt into:

::

   git clone https://github.com/jstemmler/pyadapt

To install, change to the newly created pyadapt directory and run the install script

::

   python setup.py install

This will install pyadapt into your system default python environment.

.. note::
   You will also need Numpy, matplotlib, and the netCDF4 python packages for pyplot to work

Import and Plot
+++++++++++++++
Now that you have pyadapt installed, it is easy to get up and running with the data.

>>> import pyadapt
>>> filename = '/home/jstemmler/data/test_arm_sfcmet_file.nc'
>>> sfc = pyadapt.read(filename)
>>> sfc.plot()

There are a couple of options that can go into the plot() method which primarily deal with plot output. For more information about that, I encourage you to browse the documentation and see what those options are.


Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
