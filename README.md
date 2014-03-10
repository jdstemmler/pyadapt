## Python ARM Data Analysis and Plotting Toolkit
### Author: Jayson Stemmler <jstemm@uw.edu>
#### Version 0.0.1 (March 09, 2014)

The Python ARM Data Analysis and Plotting Toolkit (Py-ADAPT) is (will be) a collection of useful tools for reading and viewing data from the Atmospheric Radiation Measurement (ARM) sites. These are tools that I have developed during the course of doing research for the University of Washington - I am not affiliated with ARM in any official capacity. Use of these tools is for informational purposes only and at your own risk. I have done my best to make sure the tools are not doing anything wonky, but feel free to browse the source if you would like.

### Installation

Installation of this package can be done using the standard python install: `python setup.py install` after cloning or forking the repository.

### Use

As of the current version, only the sounding files are supported. More will be supported in future releases, but right now it's just the soundings. The following provides a quick example of how to get up and running to view a sounding and get some of the data:

	import pyadapt
	f = '/your/data/location/souding_file.cdf'
	SND = pyadapt.read(f)

The SND object contains several methods:

	In [4]: dir(SND)
	Out[4]: 
	['__doc__',
 	'__init__',
 	'__module__',
 	'data',
 	'dimensions',
 	'keys',
 	'long_name',
 	'missing_value',
 	'plot',
 	'units']

The methods data, dimensions, long_name, missing_value, and units are each a keyed dictionary, containing the keys listed in SND.keys. For example, if you wanted the dry-bulb temperature data you could do `tdry = SND.data['tdry']` to get it. Same thing to get the missing values or dimensions or long names of things. 

The actual data contained inside `SND.data` is, in the presence of a matching `SND.missing_value` value, a Numpy masked array. This tries to mask out the invalid values, and I just wanted you to be aware of that.

#### Plotting

This is where, in my opinion, this module will really shine. If you simply make a call to

	SND.plot()

you'll get a nicely (eventually...) formated plot for you to check out the data. In the case of the sounding data, this takes the form of a sounding with temperature and dewpoint and another panel with RH. So really, with three lines of code, you can have a look at the data. Example plot and the code is shown.

	import pyadapt
	SND = pyadapt.read('/your/data/location/souding_file.cdf')
	SND.plot(altmax=5000, out='snd_out.png')

![Example Sounding](https://raw.github.com/jstemmler/pyadapt/master/examples/snd_out.png)

### Feedback

Feedback can be sent to Jayson Stemmler (<jstemm@uw.edu>) although I might not get back to you in a quick and timely manner. Thanks for checking out the repository!
