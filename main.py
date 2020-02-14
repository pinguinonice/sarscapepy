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
#filename='D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S22D/PSI_PS_processing/geocoding/PSI_PS_60_0_VD.shp'
df = geopandas.read_file(filename)
#interpolate to grid
grid=shape2grid(dataFrame=df, values='Velocity', gridSize=1/3600, LonMin=14.00,LonMax=14.06,LatMin=45.98,LatMax=46.04, method='linear')


# display on basemap
import numpy as np
import georaster

# load basemap
base_path="basemap/Idrija_14.tif"
base = georaster.MultiBandRaster(base_path)

# load grid as georeferenced
velocity = georaster.SingleBandRaster.from_array(grid.get('Velocity'), grid.get('info').get('geoTransform'), grid.get('info').get('projection'))



# plot
fig, ax = plt.subplots()

plt.imshow(np.array(base.r[:,:,:], dtype='uint8')  , alpha=1,extent=base.extent)
plt.xlabel('Lon')
plt.ylabel('Lat')
plot_grid=plt.imshow(np.array(velocity.r)  , alpha=0.6, cmap='RdBu',extent=velocity.extent)
plt.clim(-20,20) 
cbar = fig.colorbar(plot_grid)

plt.ylim(plt.ylim()[::-1])
plt.show()




