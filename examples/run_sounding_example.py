import pyadapt
import os

f = os.path.join('./data/grwsondewnpnM1.b1.20100531.112900.cdf')

snd = pyadapt.read(f)
snd.plot(ptop=100, plot_output=True, autoname=True, skew=90)