import pyadapt
f = '/Users/jstemm/Documents/research/data/test/grwsondewnpnM1.b1.20100531.112900.cdf'
snd = pyadapt.read(f)
snd.plot(altmax=7000)
