import pyadapt
import os

file_in = os.path.abspath('./data/grwsondewnpnM1.b1.20100531.112900.cdf')
plot_dir = os.path.abspath('./plots')

snd = pyadapt.read(file_in)
snd.plot(ptop=100,
         plot_output=True,
         out_dir = plot_dir,
         autoname=True,
         skew=90)