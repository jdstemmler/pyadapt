## Python ARM Data Analysis and Plotting Toolkit
### Author: Jayson Stemmler <jstemm@uw.edu>
#### Version 0.0.1 (March 20, 2014)

#####NOTE: (2015 Jan 06)
After some stalled development on this project, I will be working to bring this up to speed with most of the instruments available at the ENA permanent site. There should be some good new features coming soon(ish)!

### Introduction

The Python ARM Data Analysis and Plotting Toolkit (Py-ADAPT) is a collection of useful tools for reading, viewing, and plotting data from the Atmospheric Radiation Measurement (ARM) sites. Use of these tools is for informational purposes only and at your own risk. I have done my best to make sure the tools are not doing anything wonky, but feel free to browse the source if you would like.

### Disclaimer

This package has been tested using files from the AMF ARM mobile deployment on Graciosa Island in the Azores (site-id: 'grw'). (note here: I am working on updating for ENA). I have not yet done any testing with files from other ARM sites or datastreams. If anyone would like to test them out and report back, that would be great. If you are having issues with a particular datastream, please submit an issue. I am more than happy to get other sites up and going with this package, and I would hope that eventually this package will work on all ARM datastreams (probably not VAPs or PI datastreams - who knows). Anyway, just a heads up that this is in no way a finished-up package yet.

### Installation and Updating

Installation of this package can be done using the standard python install: 
	
	python setup.py install
	
This step should be done after cloning or forking the repo into a directory of your choice. This command will install python into the system python path - I highly recommend using the Anaconda python distribution. This makes things much easier for installation.

**To update the package, follow one of the two steps below:**

##### If you have cloned the repository via git:
1. run a quick `git pull` from the master branch to update the source code
2. then you can `python setup.py install` to update the copy in your local python distribution.

##### If you have forked the repository:
This could be a little more challenging, depending on what work you've done. If you've made modifications to files included in the repository, chances are that there will be merge conflicts between your edits and mine. If you know what that means, you probably know how to update your package at this moment. I will provide further instructions in a future update.

### Example Data
You can [download some example data](https://www.dropbox.com/s/8nwbker7jxsni2k/pyadapt_example_files.zip?dl=0) as a zip file and play around with it. This data comes from the [ARM Data Archive](http://www.archive.arm.gov/) from the Graciosa Island Field campaign. Included are four sounding files, one surface meteorology file, and one aerosol file. As functionality is built out on the site, more example data will be included.

### More Information

For examples and easy-to-read use instructions, please refer to the wiki. I will attempt to keep this updated as more features are added. If there's something you would like to see there, let me know.

For documentation of the code, please visit <http://jstemmler.github.io/pyadapt/>. This contains documentation for all of the modules, submodules, and classes utilized within this package. It will probably be the most up-to-date.

### Feedback

Feedback can be sent to Jayson Stemmler (<jstemm@uw.edu>) although I might not get back to you in a quick and timely manner. Thanks for checking out the repository!
