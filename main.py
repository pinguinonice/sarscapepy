#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:16:02 2020

@author: pippo
"""

import geopandas

import matplotlib.pyplot as plt

from sarscapepy import shape2grid


# read file
#filename= input('Enter Shape file name please : ')
filename= 'D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/PS_S44A/PSI_PS_processing/geocoding/PSI_PS_60_0_VD.shp'
df = geopandas.read_file(filename)


#interpolate to grid

grid=shape2grid(dataFrame=df, value='Velocity', gridSize=1/3600, Xmin=None, Xmax=None, Ymin=None, Ymax=None, method='linear', fillValue=0)


# display






# Show
plt.figimage(grid)
plt.show()


