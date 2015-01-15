import pyadapt
import os

file_in = os.path.abspath('./data/grwmetM1.b1.20100531.000000.cdf')
plot_dir = os.path.abspath('./plots')

SFC = pyadapt.read(file_in)
SFC.plot(plot_output=True, out_dir=plot_dir)