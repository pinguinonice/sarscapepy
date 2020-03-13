# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:53:17 2020

@author: philipp
"""

from sarscapepy import shape2grid, dispGrid, read_file,interpolateTemporal

# read file
#filename= input('Enter Shape file name please : ')
filename= 'D:/Philipp/5-Projects/STINGS/Idrija/Project 2020/Idrija/PS_S44A/PSI_PS_processing/geocoding/PSI_PS_60_0.shp'

df = read_file(filename)


#interpolate to grid
grid=shape2grid(dataFrame=df, values=None, gridSize=1/3600, LonMin=14.00,LonMax=14.06,LatMin=45.98,LatMax=46.04, method='linear')

timeStart = '20170101'
timeEnd ='20200101'
timeStepDays=30 #days
kind= 'cubic' #‘linear’, ‘nearest’, ‘zero’, ‘slinear’, ‘quadratic’, ‘cubic’, ‘previous’, ‘next’
grid =interpolateTemporal(grid, timeStart, timeEnd, timeStepDays, kind =kind)


# input
base_path="basemap/Idrija_14.tif"
clim=(-50,50)

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import georaster




DateStrigns=[key for key in grid.keys() if 'D_' in key[0:2]]



def init():
    fig,ax = plt.subplots()

    ax.set_title(DateStrigns[0])
    
    if type(base_path) == str:
        # load basemap
        base = georaster.MultiBandRaster(base_path)
        plot_base=plt.imshow(np.array(base.r[:,:,:], dtype='uint8')  , alpha=1,extent=base.extent)
    
    layer = georaster.SingleBandRaster.from_array(grid.get(DateStrigns[0]), grid.get('info').get('geoTransform'), grid.get('info').get('projection'))   
    plot_grid=ax.imshow(np.array(layer.r)  , alpha=0.6, cmap='RdBu',extent=layer.extent)
    cbar = fig.colorbar(plot_grid)
    plot_grid.set_clim(clim[0],clim[1]) 
    return plot_grid




def animate(i):
    layer = georaster.SingleBandRaster.from_array(grid.get(DateStrigns[i]), grid.get('info').get('geoTransform'), grid.get('info').get('projection'))   
    plot_grid.set_data(np.array(layer.r))
    plot_grid.set_clim(clim[0],clim[1])  
    ax.set_title(DateStrigns[i])
    plt.pause(0.5)
    return plot_grid

anim = FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)


anim.save('sine_wave.gif', writer='imagemagick')