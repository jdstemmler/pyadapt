# -*- coding: utf-8 -*-

import pyadapt
import os

file_in = os.path.abspath('./data/grwaosM1.a1.20100531.000000.cdf')
plot_dir = os.path.abspath('./plots')

F = pyadapt.read(file_in)
F.plot(save_plot=True, out_dir=plot_dir)