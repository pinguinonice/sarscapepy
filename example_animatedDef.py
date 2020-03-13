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


base_path="basemap/Idrija_14.tif"
clim=(-50,50)
import numpy as np
import georaster
import matplotlib.pyplot as plt
import georaster
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

DateStrigns=[key for key in grid.keys() if 'D_' in key[0:2]]
    
# new plot 
fig, ax = plt.subplots()
        

title = ax.text(0.5,1.05,DateStrigns[0], 
                    size=plt.rcParams["axes.titlesize"],
                    ha="center", transform=ax.transAxes, )
# if basemap path is set
if type(base_path) == str:
    # load basemap
    base = georaster.MultiBandRaster(base_path)
    plot_base=plt.imshow(np.array(base.r[:,:,:], dtype='uint8')  , alpha=1,extent=base.extent)

layer = georaster.SingleBandRaster.from_array(grid.get(DateStrigns[0]), grid.get('info').get('geoTransform'), grid.get('info').get('projection'))   
plot_grid=plt.imshow(np.array(layer.r)  , alpha=0.6, cmap='RdBu',extent=layer.extent)

#check if there is more than one axes
cbar = fig.colorbar(plot_grid)
    

# label axis
plt.xlabel('Lon')
plt.ylabel('Lat')

# flip Lat axis
if plt.ylim()[0]>plt.ylim()[1]:
   plt.ylim(plt.ylim()[::-1])


#fig.canvas.manager.window.raise_()

# frame grabbing  initialysed
ims=[]
ims.append([plot_grid,title])

for DateString in DateStrigns[1:]:
    layer = georaster.SingleBandRaster.from_array(grid.get(DateString), grid.get('info').get('geoTransform'), grid.get('info').get('projection'))   
    plot_grid=plt.imshow(np.array(layer.r)  , alpha=0.6, cmap='RdBu',extent=layer.extent)
    plot_grid.set_clim(clim[0],clim[1])  
    title.set_text( DateString )
    
    
    # grab frame
    ims.append([plot_grid,title])


ani = animation.ArtistAnimation(fig, ims, interval=10, repeat_delay=1000)

writer = PillowWriter(fps=20)
ani.save("sss.gif", writer=writer)






