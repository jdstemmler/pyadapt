import pyadapt
import os

f = os.path.join('./data/grwmetM1.b1.20100531.000000.cdf')

SFC = pyadapt.read(f)
SFC.plot(plot_output=True)
