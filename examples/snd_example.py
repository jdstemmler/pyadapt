import pyadapt
f = '/Users/jstemm/Documents/research/data/test/grwsondewnpnM1.b1.20100531.112900.cdf'
snd = pyadapt.read(f)
snd.plot(ptop=100, plot_output=True, autoname=True, skew=90, out_dir = '/Users/jstemm/Documents/pyadapt/examples/')
