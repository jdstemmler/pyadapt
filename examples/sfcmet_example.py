import pyadapt
f = '/home/jstemm/Documents/research/data/sfcmet/grwmetM1.b1.20100531.000000.cdf'
SFC = pyadapt.read(f)
SFC.plot()
