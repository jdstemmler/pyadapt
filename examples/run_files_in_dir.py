# -*- coding: utf-8 -*-
import pyadapt
import glob
import os

file_dir = os.path.abspath('data')

g = glob.glob(os.path.join(file_dir, '*'))

for i in g:
    F = pyadapt.read(i)
    F.plot(plot_output=True, out_dir=os.path.abspath('plots'))